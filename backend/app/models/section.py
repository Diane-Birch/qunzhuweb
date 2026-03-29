from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class SiteSection(BaseModel, SortableActiveMixin):
    """Structured section content for homepage text, images, stats and tags."""

    __tablename__ = "site_sections"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(80), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, nullable=True, index=True)
    node_type = Column(String(20), nullable=False, default="content")
    content_source = Column(String(20), nullable=True)
    group_key = Column(String(80), nullable=True)
    name = Column(String(120), nullable=False)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(255), nullable=True)
    summary = Column(String(500), nullable=True)
    body = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    media_type = Column(String(20), nullable=True)
    video_url = Column(String(500), nullable=True)
    extra_json = Column(Text, nullable=True)
    pinned_at = Column(DateTime, nullable=True)

