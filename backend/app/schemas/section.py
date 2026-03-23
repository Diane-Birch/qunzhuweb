from typing import Literal, Optional

from pydantic import BaseModel, Field, root_validator

from backend.app.schemas.common import TimestampSchema


MediaType = Literal["image", "video"]


class SectionBase(BaseModel):
    key: str = Field(..., min_length=2, max_length=80)
    name: str = Field(..., min_length=1, max_length=120)
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    media_type: MediaType = "image"
    video_url: Optional[str] = Field(None, max_length=500)
    extra_json: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

    @root_validator
    def validate_video_media(cls, values):
        values["media_type"] = values.get("media_type") or "image"
        if values["media_type"] == "video" and not values.get("video_url"):
            raise ValueError("Video url is required when media_type is video")
        return values


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class SectionRead(SectionBase, TimestampSchema):
    pass
