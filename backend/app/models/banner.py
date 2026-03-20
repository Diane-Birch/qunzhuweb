from sqlalchemy import Column, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class HeroBanner(BaseModel, SortableActiveMixin):
    """Homepage banner content shown in the front-end carousel."""

    __tablename__ = "hero_banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=False)
    cta_text = Column(String(100), nullable=True)
    cta_link = Column(String(255), nullable=True)
