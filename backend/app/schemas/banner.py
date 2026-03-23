from typing import Literal, Optional

from pydantic import BaseModel, Field, root_validator

from backend.app.schemas.common import TimestampSchema


MediaType = Literal["image", "video"]
TextPosition = Literal[
    "left-center",
    "center",
    "right-center",
    "left-bottom",
    "center-bottom",
    "right-bottom",
    "left-top",
    "center-top",
    "right-top",
]


class BannerBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    media_type: MediaType = "image"
    video_url: Optional[str] = Field(None, max_length=500)
    cta_text: Optional[str] = Field(None, max_length=100)
    cta_link: Optional[str] = Field(None, max_length=255)
    title_font_size: int = Field(72, ge=12, le=160)
    subtitle_font_size: int = Field(13, ge=10, le=72)
    description_font_size: int = Field(17, ge=10, le=72)
    text_position: TextPosition = "left-center"
    sort_order: int = 0
    is_active: bool = True

    @root_validator
    def validate_banner_media(cls, values):
        values["media_type"] = values.get("media_type") or "image"
        values["title_font_size"] = values.get("title_font_size") or 72
        values["subtitle_font_size"] = values.get("subtitle_font_size") or 13
        values["description_font_size"] = values.get("description_font_size") or 17
        values["text_position"] = values.get("text_position") or "left-center"

        if values["media_type"] == "video" and not values.get("video_url"):
            raise ValueError("Video url is required when media_type is video")
        if values["media_type"] == "image" and not values.get("image_url"):
            raise ValueError("Image url is required when media_type is image")
        return values


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass


class BannerRead(BannerBase, TimestampSchema):
    pass
