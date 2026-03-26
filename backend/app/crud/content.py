from typing import Optional, Type

from sqlalchemy import asc, case, desc, or_
from sqlalchemy.orm import Query, Session

from backend.app.schemas.common import PageParams, PageResult


def apply_keyword_filter(query: Query, model: Type, keyword: Optional[str], fields):
    """Apply keyword search on one or more text columns when the caller provides a term."""
    if not keyword:
        return query
    conditions = [getattr(model, field).like(f"%{keyword}%") for field in fields]
    return query.filter(or_(*conditions))


def paginate(query: Query, params: PageParams, model: Type, order_field: str):
    """Return paginated results with a stable order for repeatable admin tables."""
    total = query.count()
    items = (
        query.order_by(asc(getattr(model, order_field)), desc(model.created_at))
        .offset((params.page - 1) * params.page_size)
        .limit(params.page_size)
        .all()
    )
    return PageResult(total=total, page=params.page, page_size=params.page_size, items=items)


def paginate_query(query: Query, params: PageParams):
    """Paginate a query that already carries its final ordering."""
    total = query.count()
    items = query.offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    return PageResult(total=total, page=params.page, page_size=params.page_size, items=items)


def apply_pinned_order(query: Query, model: Type, *recency_fields: str):
    """Pinned content first, then newest content by the provided recency fields."""
    pinned_rank = case((getattr(model, "sort_order") == 0, 0), else_=1)
    order_fields = [pinned_rank.asc(), desc(getattr(model, "pinned_at"))]
    for field_name in recency_fields:
        order_fields.append(desc(getattr(model, field_name)))
    if "id" not in recency_fields:
        order_fields.append(desc(getattr(model, "id")))
    return query.order_by(*order_fields)


def apply_section_content_order(query: Query, model: Type):
    return apply_pinned_order(query, model, "created_at", "id")


def create_record(db: Session, model: Type, payload):
    """Create a new SQLAlchemy entity from the validated request schema."""
    record = model(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_record(db: Session, record, payload):
    """Update an existing entity in place using the validated request schema."""
    for field, value in payload.dict().items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record):
    """Delete the provided entity and persist the change immediately."""
    db.delete(record)
    db.commit()
