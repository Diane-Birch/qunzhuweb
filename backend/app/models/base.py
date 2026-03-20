from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from backend.app.core.database import Base


class TimestampMixin:
    """Shared timestamp columns for all persistent entities."""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class SortableActiveMixin:
    """Shared columns used by content records that support ordering and publishing."""

    sort_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class BaseModel(Base, TimestampMixin):
    """Base model to keep all ORM classes consistent."""

    __abstract__ = True
