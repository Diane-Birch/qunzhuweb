from types import SimpleNamespace

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.database import get_db
from backend.app.models.banner import HeroBanner
from backend.app.models.footer_qr_code import FooterQRCode
from backend.app.models.news import NewsArticle
from backend.app.models.product import Product
from backend.app.models.section import SiteSection
from backend.app.models.site_setting import SiteSetting
from backend.app.schemas.news import NewsRead
from backend.app.schemas.product import ProductRead
from backend.app.schemas.public import HomePageResponse
from backend.app.schemas.section import SectionRead


router = APIRouter(prefix="/public", tags=["public"])

LEGACY_FOOTER_QR_KEY = "footer_qr"
FOOTER_FILING_KEY = "footer_filing"
EXCLUDED_SECTION_KEYS = ["product_intro", "news_intro"]


def get_footer_qr_codes(db: Session):
    qr_codes = (
        db.query(FooterQRCode)
        .filter(FooterQRCode.is_active.is_(True))
        .order_by(FooterQRCode.sort_order.asc(), FooterQRCode.created_at.desc())
        .all()
    )
    if qr_codes:
        return qr_codes

    legacy_qr = (
        db.query(SiteSetting)
        .filter(
            SiteSetting.key == LEGACY_FOOTER_QR_KEY,
            SiteSetting.is_active.is_(True),
            SiteSetting.image_url.isnot(None),
        )
        .first()
    )
    if not legacy_qr:
        return []

    return [
        SimpleNamespace(
            id=legacy_qr.id,
            name=legacy_qr.name,
            description=legacy_qr.description,
            image_url=legacy_qr.image_url,
            sort_order=0,
            is_active=legacy_qr.is_active,
            created_at=legacy_qr.created_at,
            updated_at=legacy_qr.updated_at,
        )
    ]


@router.get("/home", response_model=HomePageResponse)
def get_homepage(db: Session = Depends(get_db)) -> HomePageResponse:
    """Aggregate all homepage content so the frontend can render from one request."""
    banners = (
        db.query(HeroBanner)
        .filter(HeroBanner.is_active.is_(True))
        .order_by(HeroBanner.sort_order.asc(), HeroBanner.created_at.desc())
        .all()
    )
    sections = (
        db.query(SiteSection)
        .filter(
            SiteSection.is_active.is_(True),
            SiteSection.key.notin_(EXCLUDED_SECTION_KEYS),
        )
        .order_by(SiteSection.sort_order.asc(), SiteSection.created_at.desc())
        .all()
    )
    products = (
        db.query(Product)
        .filter(Product.is_active.is_(True))
        .order_by(Product.sort_order.asc(), Product.created_at.desc())
        .all()
    )
    news = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_active.is_(True))
        .order_by(NewsArticle.sort_order.asc(), NewsArticle.published_at.desc())
        .all()
    )
    product_intro = (
        db.query(SiteSection)
        .filter(SiteSection.key == "product_intro", SiteSection.is_active.is_(True))
        .first()
    )
    news_intro = (
        db.query(SiteSection)
        .filter(SiteSection.key == "news_intro", SiteSection.is_active.is_(True))
        .first()
    )
    footer_filing = (
        db.query(SiteSetting)
        .filter(SiteSetting.key == FOOTER_FILING_KEY, SiteSetting.is_active.is_(True))
        .first()
    )

    return HomePageResponse(
        banners=banners,
        sections=sections,
        products=products,
        news=news,
        product_intro=product_intro,
        news_intro=news_intro,
        footer_qr_codes=get_footer_qr_codes(db),
        footer_filing=footer_filing,
    )


@router.get("/sections/{section_key}", response_model=SectionRead)
def get_public_section_detail(section_key: str, db: Session = Depends(get_db)) -> SectionRead:
    section = (
        db.query(SiteSection)
        .filter(SiteSection.key == section_key, SiteSection.is_active.is_(True))
        .first()
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.get("/products/{product_id}", response_model=ProductRead)
def get_public_product_detail(product_id: int, db: Session = Depends(get_db)) -> ProductRead:
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_active.is_(True))
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/news/{news_id}", response_model=NewsRead)
def get_public_news_detail(news_id: int, db: Session = Depends(get_db)) -> NewsRead:
    article = (
        db.query(NewsArticle)
        .filter(NewsArticle.id == news_id, NewsArticle.is_active.is_(True))
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article
