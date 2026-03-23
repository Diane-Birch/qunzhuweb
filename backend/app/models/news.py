from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class NewsArticle(BaseModel, SortableActiveMixin):
    """News and enterprise updates displayed on the public homepage."""

    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    media_type = Column(String(20), nullable=True)
    video_url = Column(String(500), nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)