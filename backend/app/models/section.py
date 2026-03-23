from sqlalchemy import Column, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class SiteSection(BaseModel, SortableActiveMixin):
    """Structured section content for homepage text, images, stats and tags."""

    __tablename__ = "site_sections"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    media_type = Column(String(20), nullable=True)
    video_url = Column(String(500), nullable=True)
    extra_json = Column(Text, nullable=True)