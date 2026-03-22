from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class SiteSettingBase(BaseModel):
    key: str = Field(..., min_length=2, max_length=80)
    name: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True


class SiteSettingCreate(SiteSettingBase):
    pass


class SiteSettingUpdate(SiteSettingBase):
    pass


class SiteSettingRead(SiteSettingBase, TimestampSchema):
    pass


class FooterSettingsRead(BaseModel):
    footer_qr: SiteSettingRead
    footer_filing: SiteSettingRead


class FooterSettingsUpdate(BaseModel):
    qr_name: Optional[str] = Field(None, max_length=120)
    qr_description: Optional[str] = Field(None, max_length=255)
    qr_image_url: Optional[str] = Field(None, max_length=500)
    qr_is_active: bool = True
    filing_name: Optional[str] = Field(None, max_length=120)
    filing_text: Optional[str] = Field(None, max_length=255)
    filing_is_active: bool = True


class UploadResponse(BaseModel):
    url: str