from typing import Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import TimestampSchema


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=160)
    subtitle: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    specs_json: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase, TimestampSchema):
    pass
