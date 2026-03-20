from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.content import (
    apply_keyword_filter,
    create_record,
    delete_record,
    paginate,
    update_record,
)
from backend.app.deps import get_current_admin
from backend.app.models.banner import HeroBanner
from backend.app.models.user import AdminUser
from backend.app.schemas.banner import BannerCreate, BannerRead, BannerUpdate
from backend.app.schemas.common import PageParams, PageResult


router = APIRouter(prefix="/banners", tags=["banners"])


@router.get("", response_model=PageResult[BannerRead])
def list_banners(
    page: int = 1,
    page_size: int = 10,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(HeroBanner), HeroBanner, keyword, ["title", "subtitle"])
    return paginate(query, PageParams(page=page, page_size=page_size, keyword=keyword), HeroBanner, "sort_order")


@router.post("", response_model=BannerRead)
def create_banner(
    payload: BannerCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return create_record(db, HeroBanner, payload)


@router.put("/{banner_id}", response_model=BannerRead)
def update_banner(
    banner_id: int,
    payload: BannerUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    banner = db.query(HeroBanner).filter(HeroBanner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return update_record(db, banner, payload)


@router.delete("/{banner_id}")
def remove_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    banner = db.query(HeroBanner).filter(HeroBanner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    delete_record(db, banner)
    return {"message": "Banner deleted"}
