from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar("T")
ADMIN_MAX_PAGE_SIZE = 200


class PageParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=ADMIN_MAX_PAGE_SIZE)
    keyword: Optional[str] = None


class PageResult(GenericModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]


class TimestampSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
