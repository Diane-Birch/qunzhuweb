import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.deps import get_current_admin
from backend.app.models.site_setting import SiteSetting
from backend.app.models.user import AdminUser
from backend.app.schemas.site_setting import FooterSettingsRead, FooterSettingsUpdate, SiteSettingRead, UploadResponse


router = APIRouter(prefix="/site-settings", tags=["site-settings"])

FOOTER_QR_KEY = "footer_qr"
FOOTER_FILING_KEY = "footer_filing"
DEFAULT_FOOTER_QR = {
    "key": FOOTER_QR_KEY,
    "name": "页脚二维码",
    "description": "扫码关注我们",
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
UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads" / "site-settings"
IMAGE_SUFFIX_MAP = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
ALLOWED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}


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
    return get_or_create_setting(db, FOOTER_QR_KEY, DEFAULT_FOOTER_QR)


def get_footer_filing_setting(db: Session) -> SiteSetting:
    return get_or_create_setting(db, FOOTER_FILING_KEY, DEFAULT_FOOTER_FILING)


@router.get("/footer-settings", response_model=FooterSettingsRead)
def get_footer_settings(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return FooterSettingsRead(
        footer_qr=SiteSettingRead.from_orm(get_footer_qr_setting(db)),
        footer_filing=SiteSettingRead.from_orm(get_footer_filing_setting(db)),
    )


@router.put("/footer-settings", response_model=FooterSettingsRead)
def update_footer_settings(
    payload: FooterSettingsUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    footer_qr = get_footer_qr_setting(db)
    footer_filing = get_footer_filing_setting(db)

    footer_qr.name = payload.qr_name or DEFAULT_FOOTER_QR["name"]
    footer_qr.description = payload.qr_description
    footer_qr.image_url = payload.qr_image_url
    footer_qr.is_active = payload.qr_is_active

    footer_filing.name = payload.filing_name or DEFAULT_FOOTER_FILING["name"]
    footer_filing.description = payload.filing_text
    footer_filing.is_active = payload.filing_is_active

    db.commit()
    db.refresh(footer_qr)
    db.refresh(footer_filing)

    return FooterSettingsRead(
        footer_qr=SiteSettingRead.from_orm(footer_qr),
        footer_filing=SiteSettingRead.from_orm(footer_filing),
    )


@router.post("/upload-image", response_model=UploadResponse)
def upload_site_setting_image(
    file: UploadFile = File(...),
    _: AdminUser = Depends(get_current_admin),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="未选择上传文件")

    content_type = file.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="仅支持上传图片文件")

    original_suffix = Path(file.filename).suffix.lower()
    suffix = original_suffix if original_suffix in ALLOWED_IMAGE_SUFFIXES else IMAGE_SUFFIX_MAP.get(content_type, ".png")

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    target_path = UPLOADS_DIR / filename

    try:
        with target_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return UploadResponse(url=f"/uploads/site-settings/{filename}")