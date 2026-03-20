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
from backend.app.models.section import SiteSection
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.section import SectionCreate, SectionRead, SectionUpdate


router = APIRouter(prefix="/sections", tags=["sections"])


@router.get("", response_model=PageResult[SectionRead])
def list_sections(
    page: int = 1,
    page_size: int = 20,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(SiteSection), SiteSection, keyword, ["name", "title", "key"])
    return paginate(query, PageParams(page=page, page_size=page_size, keyword=keyword), SiteSection, "sort_order")


@router.post("", response_model=SectionRead)
def create_section(
    payload: SectionCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    exists = db.query(SiteSection).filter(SiteSection.key == payload.key).first()
    if exists:
        raise HTTPException(status_code=400, detail="Section key already exists")
    return create_record(db, SiteSection, payload)


@router.put("/{section_id}", response_model=SectionRead)
def update_section(
    section_id: int,
    payload: SectionUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    section = db.query(SiteSection).filter(SiteSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    duplicate = (
        db.query(SiteSection)
        .filter(SiteSection.key == payload.key, SiteSection.id != section_id)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=400, detail="Section key already exists")
    return update_record(db, section, payload)


@router.delete("/{section_id}")
def remove_section(
    section_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    section = db.query(SiteSection).filter(SiteSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    delete_record(db, section)
    return {"message": "Section deleted"}
