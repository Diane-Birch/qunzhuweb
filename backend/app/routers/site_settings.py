from pathlib import Path
import shutil
from types import SimpleNamespace
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.deps import get_current_admin
from backend.app.models.footer_qr_code import FooterQRCode
from backend.app.models.site_setting import SiteSetting
from backend.app.models.user import AdminUser
from backend.app.schemas.site_setting import FooterSettingsRead, FooterSettingsUpdate, SiteSettingRead, UploadResponse


router = APIRouter(prefix="/site-settings", tags=["site-settings"])

LEGACY_FOOTER_QR_KEY = "footer_qr"
FOOTER_FILING_KEY = "footer_filing"
DEFAULT_FOOTER_QR = {
    "key": LEGACY_FOOTER_QR_KEY,
    "name": "扫码关注我们",
    "description": "获取最新红河文化信息",
    "image_url": None,
    "is_active": True,
}
DEFAULT_FOOTER_FILING = {
    "key": FOOTER_FILING_KEY,
    "name": "备案信息",
    "description": "",
    "image_url": None,
    "is_active": True,
}
UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads"
IMAGE_SUFFIX_MAP = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
VIDEO_SUFFIX_MAP = {
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "video/ogg": ".ogv",
    "video/quicktime": ".mov",
    "video/x-m4v": ".m4v",
}
ALLOWED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
ALLOWED_VIDEO_SUFFIXES = {".mp4", ".webm", ".ogv", ".mov", ".m4v"}


def get_or_create_setting(db: Session, key: str, defaults: dict) -> SiteSetting:
    setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if setting:
        return setting

    setting = SiteSetting(**defaults)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def get_footer_qr_setting(db: Session) -> SiteSetting:
    return get_or_create_setting(db, LEGACY_FOOTER_QR_KEY, DEFAULT_FOOTER_QR)


def get_footer_filing_setting(db: Session) -> SiteSetting:
    return get_or_create_setting(db, FOOTER_FILING_KEY, DEFAULT_FOOTER_FILING)


def build_legacy_qr_code(db: Session):
    legacy_qr = get_footer_qr_setting(db)
    if not any([legacy_qr.name, legacy_qr.description, legacy_qr.image_url]):
        return None

    return SimpleNamespace(
        id=0,
        name=legacy_qr.name,
        description=legacy_qr.description,
        image_url=legacy_qr.image_url,
        sort_order=0,
        is_active=legacy_qr.is_active,
        created_at=legacy_qr.created_at,
        updated_at=legacy_qr.updated_at,
    )


def list_footer_qr_codes_for_admin(db: Session):
    qr_codes = (
        db.query(FooterQRCode)
        .order_by(FooterQRCode.sort_order.asc(), FooterQRCode.created_at.desc())
        .all()
    )
    if qr_codes:
        return qr_codes

    legacy_qr = build_legacy_qr_code(db)
    return [legacy_qr] if legacy_qr else []


def sync_footer_qr_codes(db: Session, payload_items):
    existing_records = {record.id: record for record in db.query(FooterQRCode).all()}
    persisted_records = []

    for index, item in enumerate(payload_items):
        record = existing_records.pop(item.id, None) if item.id else None
        if record is None:
            record = FooterQRCode()
            db.add(record)

        record.name = item.name
        record.description = item.description
        record.image_url = item.image_url
        record.sort_order = item.sort_order if item.sort_order is not None else index
        record.is_active = item.is_active
        persisted_records.append(record)

    for stale_record in existing_records.values():
        db.delete(stale_record)

    db.flush()
    return sorted(persisted_records, key=lambda record: (record.sort_order, record.id or 0))


def sync_legacy_footer_qr(db: Session, qr_codes):
    legacy_qr = get_footer_qr_setting(db)
    primary_qr = next((item for item in qr_codes if item.is_active and item.image_url), qr_codes[0] if qr_codes else None)

    if primary_qr is None:
        legacy_qr.name = DEFAULT_FOOTER_QR["name"]
        legacy_qr.description = ""
        legacy_qr.image_url = None
        legacy_qr.is_active = False
        return legacy_qr

    legacy_qr.name = primary_qr.name or DEFAULT_FOOTER_QR["name"]
    legacy_qr.description = primary_qr.description
    legacy_qr.image_url = primary_qr.image_url
    legacy_qr.is_active = primary_qr.is_active
    return legacy_qr


def save_media_file(file: UploadFile, media_type: str) -> UploadResponse:
    content_type = file.content_type or ""
    original_suffix = Path(file.filename or "").suffix.lower()

    if media_type == "image":
        if not content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed for image uploads")
        suffix = original_suffix if original_suffix in ALLOWED_IMAGE_SUFFIXES else IMAGE_SUFFIX_MAP.get(content_type, ".png")
        subdir = "images"
    else:
        if not content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail="Only video files are allowed for video uploads")
        suffix = original_suffix if original_suffix in ALLOWED_VIDEO_SUFFIXES else VIDEO_SUFFIX_MAP.get(content_type, ".mp4")
        subdir = "videos"

    target_dir = UPLOADS_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    target_path = target_dir / filename

    try:
        with target_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return UploadResponse(url=f"/uploads/{subdir}/{filename}", media_type=media_type)


@router.get("/footer-settings", response_model=FooterSettingsRead)
def get_footer_settings(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return FooterSettingsRead(
        footer_qr_codes=list_footer_qr_codes_for_admin(db),
        footer_filing=SiteSettingRead.from_orm(get_footer_filing_setting(db)),
    )


@router.put("/footer-settings", response_model=FooterSettingsRead)
def update_footer_settings(
    payload: FooterSettingsUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    footer_filing = get_footer_filing_setting(db)
    footer_filing.name = payload.filing_name or DEFAULT_FOOTER_FILING["name"]
    footer_filing.description = payload.filing_text
    footer_filing.is_active = payload.filing_is_active

    qr_codes = sync_footer_qr_codes(db, payload.qr_codes)
    sync_legacy_footer_qr(db, qr_codes)

    db.commit()

    return FooterSettingsRead(
        footer_qr_codes=list_footer_qr_codes_for_admin(db),
        footer_filing=SiteSettingRead.from_orm(get_footer_filing_setting(db)),
    )


@router.post("/upload-media", response_model=UploadResponse)
def upload_media_asset(
    file: UploadFile = File(...),
    media_type: str = Query("image", pattern="^(image|video)$"),
    _: AdminUser = Depends(get_current_admin),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was selected")
    return save_media_file(file, media_type)


@router.post("/upload-image", response_model=UploadResponse)
def upload_site_setting_image(
    file: UploadFile = File(...),
    _: AdminUser = Depends(get_current_admin),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was selected")
    return save_media_file(file, "image")

