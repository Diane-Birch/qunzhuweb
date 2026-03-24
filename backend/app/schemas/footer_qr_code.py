from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class FooterQRCodeBase(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, max_length=500)
    sort_order: int = 0
    is_active: bool = True


class FooterQRCodeUpdate(FooterQRCodeBase):
    id: Optional[int] = None


class FooterQRCodeRead(FooterQRCodeBase, TimestampSchema):
    pass
