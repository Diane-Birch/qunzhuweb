from typing import List, Optional

from pydantic import BaseModel

from backend.app.schemas.banner import BannerRead
from backend.app.schemas.news import NewsRead
from backend.app.schemas.product import ProductRead
from backend.app.schemas.section import SectionRead
from backend.app.schemas.site_setting import SiteSettingRead


class HomePageResponse(BaseModel):
    banners: List[BannerRead]
    sections: List[SectionRead]
    products: List[ProductRead]
    news: List[NewsRead]
    product_intro: Optional[SectionRead] = None
    news_intro: Optional[SectionRead] = None
    footer_qr: Optional[SiteSettingRead] = None
    footer_filing: Optional[SiteSettingRead] = None