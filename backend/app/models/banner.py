from sqlalchemy import Column, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class HeroBanner(BaseModel, SortableActiveMixin):
    """Homepage banner content shown in the front-end carousel."""

    __tablename__ = "hero_banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    media_type = Column(String(20), nullable=True)
    video_url = Column(String(500), nullable=True)
    cta_text = Column(String(100), nullable=True)
    cta_link = Column(String(255), nullable=True)
    title_font_size = Column(Integer, nullable=True)
    subtitle_font_size = Column(Integer, nullable=True)
    description_font_size = Column(Integer, nullable=True)
    text_position = Column(String(40), nullable=True)