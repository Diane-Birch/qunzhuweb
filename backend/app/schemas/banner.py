from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class BannerBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: str = Field(..., max_length=500)
    cta_text: Optional[str] = Field(None, max_length=100)
    cta_link: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0
    is_active: bool = True


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass


class BannerRead(BannerBase, TimestampSchema):
    pass
