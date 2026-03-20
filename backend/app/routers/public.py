from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.banner import HeroBanner
from backend.app.models.news import NewsArticle
from backend.app.models.product import Product
from backend.app.models.section import SiteSection
from backend.app.schemas.public import HomePageResponse
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/public", tags=["public"])


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
            SiteSection.key.notin_(["product_intro", "news_intro"]),
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
    return HomePageResponse(
        banners=banners,
        sections=sections,
        products=products,
        news=news,
        product_intro=product_intro,
        news_intro=news_intro,
    )
