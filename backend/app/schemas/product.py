from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, root_validator

from backend.app.schemas.common import TimestampSchema


MediaType = Literal["image", "video"]


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=160)
    subtitle: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    media_type: MediaType = "image"
    video_url: Optional[str] = Field(None, max_length=500)
    specs_json: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

    @root_validator
    def validate_video_media(cls, values):
        values["media_type"] = values.get("media_type") or "image"
        if values["media_type"] == "video" and not values.get("video_url"):
            raise ValueError("Video url is required when media_type is video")
        return values


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase, TimestampSchema):
    pinned_at: Optional[datetime] = None
