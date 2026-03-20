from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class SectionBase(BaseModel):
    key: str = Field(..., min_length=2, max_length=80)
    name: str = Field(..., min_length=1, max_length=120)
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    extra_json: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class SectionRead(SectionBase, TimestampSchema):
    pass
