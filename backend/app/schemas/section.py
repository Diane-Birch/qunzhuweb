from typing import Literal, Optional

from pydantic import BaseModel, Field, root_validator

from backend.app.schemas.common import TimestampSchema


MediaType = Literal["image", "video"]
SectionNodeType = Literal["section", "content"]
SectionContentSource = Literal["section", "product", "news"]
SECTION_CONTENT_GROUPS = ("section-1", "section-2", "section-3")
SECTION_CONTENT_SOURCES = ("section", "product", "news")
SECTION_ROOT_DEFAULTS = (
    {
        "key": "section-1",
        "name": "区域 1",
        "title": "区域 1",
        "subtitle": "首页区域 1",
        "summary": "首页区域 1",
        "sort_order": 1,
        "content_source": "section",
        "legacy_keys": ("core_selling",),
    },
    {
        "key": "section-2",
        "name": "区域 2",
        "title": "区域 2",
        "subtitle": "首页区域 2",
        "summary": "首页区域 2",
        "sort_order": 2,
        "content_source": "section",
        "legacy_keys": ("brand_story",),
    },
    {
        "key": "section-3",
        "name": "区域 3",
        "title": "区域 3",
        "subtitle": "首页区域 3",
        "summary": "首页区域 3",
        "sort_order": 3,
        "content_source": "section",
        "legacy_keys": ("revitalization",),
    },
    {
        "key": "section-4",
        "name": "产品区域",
        "title": "产品区域",
        "subtitle": "首页产品区域",
        "summary": "首页产品区域",
        "sort_order": 4,
        "content_source": "product",
        "legacy_keys": ("product_intro",),
    },
    {
        "key": "section-5",
        "name": "动态区域",
        "title": "动态区域",
        "subtitle": "首页动态区域",
        "summary": "首页动态区域",
        "sort_order": 5,
        "content_source": "news",
        "legacy_keys": ("news_intro",),
    },
)


def normalize_section_key(value: Optional[str]) -> str:
    raw = str(value or "").strip()
    return raw[1:] if raw.startswith("#") else raw


class SectionBase(BaseModel):
    key: str = Field("", max_length=80)
    parent_id: Optional[int] = None
    node_type: SectionNodeType = "content"
    content_source: Optional[SectionContentSource] = None
    group_key: Optional[str] = Field(None, max_length=80)
    name: str = Field(..., min_length=1, max_length=120)
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = Field(None, max_length=500)
    body: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    media_type: MediaType = "image"
    video_url: Optional[str] = Field(None, max_length=500)
    extra_json: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

    @root_validator
    def validate_video_media(cls, values):
        values["key"] = normalize_section_key(values.get("key"))
        values["group_key"] = normalize_section_key(values.get("group_key"))
        values["node_type"] = values.get("node_type") or "content"
        values["media_type"] = values.get("media_type") or "image"
        if values["node_type"] == "section" and not values["key"]:
            raise ValueError("Section key is required")
        if values["media_type"] == "video" and not values.get("video_url"):
            raise ValueError("Video url is required when media_type is video")
        return values


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class SectionRead(SectionBase, TimestampSchema):
    pass


class SectionRootCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = Field(None, max_length=500)
    key: Optional[str] = Field(None, max_length=80)
    sort_order: int = 0
    is_active: bool = True

    @root_validator
    def normalize_key(cls, values):
        values["key"] = normalize_section_key(values.get("key"))
        return values


class SectionRootUpdate(SectionRootCreate):
    pass


class SectionRootRead(SectionRead):
    content_count: int = 0
