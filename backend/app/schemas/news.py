from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class NewsBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    published_at: datetime = Field(default_factory=datetime.utcnow)
    sort_order: int = 0
    is_active: bool = True


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsRead(NewsBase, TimestampSchema):
    pass
