from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.content import (
    apply_keyword_filter,
    apply_section_content_order,
    create_record,
    delete_record,
    paginate,
    paginate_query,
    update_record,
)
from backend.app.deps import get_current_admin
from backend.app.models.news import NewsArticle
from backend.app.models.product import Product
from backend.app.models.section import SiteSection
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.section import (
    SectionCreate,
    SectionRead,
    SectionRootCreate,
    SectionRootRead,
    SectionRootUpdate,
    SectionUpdate,
    normalize_section_key,
)


router = APIRouter(prefix="/sections", tags=["sections"])


def build_section_key_filter(key: str):
    normalized = normalize_section_key(key)
    prefixed = f"#{normalized}"
    return or_(
        SiteSection.key == normalized,
        SiteSection.key == prefixed,
        func.trim(SiteSection.key) == normalized,
        func.trim(SiteSection.key) == prefixed,
    )


def build_section_group_filter(group_key: str):
    normalized = normalize_section_key(group_key)
    prefixed = f"#{normalized}"
    return or_(
        SiteSection.group_key == normalized,
        SiteSection.group_key == prefixed,
        func.trim(SiteSection.group_key) == normalized,
        func.trim(SiteSection.group_key) == prefixed,
    )


def generate_content_key(parent: SiteSection, title: str) -> str:
    normalized_parent = normalize_section_key(parent.key) or "section"
    token = uuid4().hex[:8]
    return f"{normalized_parent}-content-{token}"


def build_publication_weight(reference_time=None) -> int:
    timestamp = int((reference_time or datetime.utcnow()).timestamp())
    return max(timestamp, 1)


def is_pinned_section(section: SiteSection) -> bool:
    return section.node_type == "content" and section.content_source == "section" and section.sort_order == 0


def next_section_root_key(db: Session) -> str:
    keys = [
        normalize_section_key(item[0])
        for item in db.query(SiteSection.key).filter(SiteSection.node_type == "section").all()
    ]
    max_index = 0
    for key in keys:
        if not key.startswith("section-"):
            continue
        suffix = key.split("-", 1)[1]
        if suffix.isdigit():
            max_index = max(max_index, int(suffix))
    return f"section-{max_index + 1}"


def get_section_root_or_404(db: Session, section_id: int) -> SiteSection:
    root = (
        db.query(SiteSection)
        .filter(SiteSection.id == section_id, SiteSection.node_type == "section")
        .first()
    )
    if not root:
        raise HTTPException(status_code=404, detail="Section root not found")
    return root


def count_root_contents(db: Session, root: SiteSection) -> int:
    if root.content_source == "product":
        return db.query(Product).count()
    if root.content_source == "news":
        return db.query(NewsArticle).count()
    return (
        db.query(SiteSection)
        .filter(
            SiteSection.node_type == "content",
            or_(
                SiteSection.parent_id == root.id,
                build_section_group_filter(root.key),
            ),
        )
        .count()
    )


@router.get("/roots", response_model=List[SectionRootRead])
def list_section_roots(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    roots = (
        db.query(SiteSection)
        .filter(SiteSection.node_type == "section")
        .order_by(SiteSection.sort_order.asc(), SiteSection.created_at.asc(), SiteSection.id.asc())
        .all()
    )
    return [
        SectionRootRead(
            **SectionRead.from_orm(root).dict(),
            content_count=count_root_contents(db, root),
        )
        for root in roots
    ]


@router.post("/roots", response_model=SectionRootRead)
def create_section_root(
    payload: SectionRootCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    key = normalize_section_key(payload.key) or next_section_root_key(db)
    duplicate = db.query(SiteSection).filter(build_section_key_filter(key)).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Section key already exists")

    root = SiteSection(
        key=key,
        parent_id=None,
        node_type="section",
        content_source="section",
        group_key=None,
        name=payload.name,
        title=payload.title,
        subtitle=payload.subtitle,
        summary=payload.summary,
        body=None,
        image_url=None,
        media_type="image",
        video_url=None,
        extra_json=None,
        sort_order=payload.sort_order,
        is_active=payload.is_active,
    )
    db.add(root)
    db.commit()
    db.refresh(root)
    return SectionRootRead(**SectionRead.from_orm(root).dict(), content_count=0)


@router.put("/roots/{section_id}", response_model=SectionRootRead)
def update_section_root(
    section_id: int,
    payload: SectionRootUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    root = get_section_root_or_404(db, section_id)
    next_key = normalize_section_key(payload.key) or root.key
    duplicate = (
        db.query(SiteSection)
        .filter(build_section_key_filter(next_key), SiteSection.id != section_id)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=400, detail="Section key already exists")

    previous_key = root.key
    root.key = next_key
    root.name = payload.name
    root.title = payload.title
    root.subtitle = payload.subtitle
    root.summary = payload.summary
    root.sort_order = payload.sort_order
    root.is_active = payload.is_active

    if root.content_source == "section" and previous_key != root.key:
        for child in db.query(SiteSection).filter(SiteSection.parent_id == root.id).all():
            child.group_key = root.key

    db.commit()
    db.refresh(root)
    return SectionRootRead(
        **SectionRead.from_orm(root).dict(),
        content_count=count_root_contents(db, root),
    )


@router.delete("/roots/{section_id}")
def remove_section_root(
    section_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    root = get_section_root_or_404(db, section_id)
    if count_root_contents(db, root):
        raise HTTPException(status_code=400, detail="Please delete child content first")
    delete_record(db, root)
    return {"message": "Section root deleted"}


@router.get("", response_model=PageResult[SectionRead])
def list_sections(
    page: int = 1,
    page_size: int = 20,
    keyword: str = None,
    group_key: str = None,
    node_type: str = "content",
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(SiteSection), SiteSection, keyword, ["name", "title", "key"])
    normalized_group_key = normalize_section_key(group_key)
    normalized_node_type = (node_type or "content").strip().lower()
    if normalized_node_type in {"section", "content"}:
        query = query.filter(SiteSection.node_type == normalized_node_type)
    if normalized_group_key:
        query = query.filter(build_section_group_filter(normalized_group_key))
    params = PageParams(page=page, page_size=page_size, keyword=keyword)
    if normalized_node_type == "content":
        query = apply_section_content_order(query, SiteSection)
        return paginate_query(query, params)
    return paginate(query, params, SiteSection, "sort_order")


@router.post("", response_model=SectionRead)
def create_section(
    payload: SectionCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    if payload.node_type == "section":
        raise HTTPException(status_code=400, detail="Use /sections/roots to create a top-level section")

    parent = None
    if payload.parent_id:
        parent = get_section_root_or_404(db, payload.parent_id)
        if parent.content_source != "section":
            raise HTTPException(status_code=400, detail="This section root uses a different content source")

    key = normalize_section_key(payload.key)
    if not key:
        if not parent:
            raise HTTPException(status_code=400, detail="Section key is required")
        key = generate_content_key(parent, payload.title)

    exists = db.query(SiteSection).filter(build_section_key_filter(key)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Section key already exists")

    payload.key = key
    payload.node_type = "content"
    payload.content_source = "section"
    payload.sort_order = build_publication_weight()
    if parent:
        payload.parent_id = parent.id
        payload.group_key = parent.key

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
    if section.node_type == "section":
        raise HTTPException(status_code=400, detail="Use /sections/roots/{id} to update a top-level section")

    duplicate = (
        db.query(SiteSection)
        .filter(build_section_key_filter(payload.key), SiteSection.id != section_id)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=400, detail="Section key already exists")

    if payload.parent_id:
        parent = get_section_root_or_404(db, payload.parent_id)
        payload.group_key = parent.key
    payload.node_type = "content"
    payload.content_source = "section"
    payload.sort_order = 0 if is_pinned_section(section) else build_publication_weight(section.created_at)
    return update_record(db, section, payload)


@router.post("/{section_id}/pin", response_model=SectionRead)
def pin_section(
    section_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    section = db.query(SiteSection).filter(SiteSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    if section.node_type != "content":
        raise HTTPException(status_code=400, detail="Only child content can be pinned")

    section.sort_order = 0
    section.pinned_at = datetime.utcnow()
    db.commit()
    db.refresh(section)
    return section


@router.post("/{section_id}/unpin", response_model=SectionRead)
def unpin_section(
    section_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    section = db.query(SiteSection).filter(SiteSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    if section.node_type != "content":
        raise HTTPException(status_code=400, detail="Only child content can be unpinned")

    section.sort_order = build_publication_weight(section.created_at)
    section.pinned_at = None
    db.commit()
    db.refresh(section)
    return section


@router.delete("/{section_id}")
def remove_section(
    section_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    section = db.query(SiteSection).filter(SiteSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    if section.node_type == "section":
        raise HTTPException(status_code=400, detail="Use /sections/roots/{id} to delete a top-level section")
    delete_record(db, section)
    return {"message": "Section deleted"}





