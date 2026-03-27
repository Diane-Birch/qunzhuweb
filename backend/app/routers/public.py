from types import SimpleNamespace

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.database import get_db
from backend.app.crud.content import apply_pinned_order, apply_section_content_order
from backend.app.models.banner import HeroBanner
from backend.app.models.footer_qr_code import FooterQRCode
from backend.app.models.news import NewsArticle
from backend.app.models.product import Product
from backend.app.models.section import SiteSection
from backend.app.models.site_setting import SiteSetting
from backend.app.schemas.common import PageResult
from backend.app.schemas.news import NewsRead
from backend.app.schemas.product import ProductRead
from backend.app.schemas.public import HomePageResponse, SectionArchiveResponse
from backend.app.schemas.section import SectionRead, normalize_section_key


router = APIRouter(prefix="/public", tags=["public"])

LEGACY_FOOTER_QR_KEY = "footer_qr"
FOOTER_FILING_KEY = "footer_filing"
HOMEPAGE_PRODUCT_LIMIT = 2
HOMEPAGE_NEWS_LIMIT = 3


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


def build_public_section_key_filter(key: str):
    normalized = normalize_section_key(key)
    prefixed = f"#{normalized}"
    return or_(
        SiteSection.key == normalized,
        SiteSection.key == prefixed,
        func.trim(SiteSection.key) == normalized,
        func.trim(SiteSection.key) == prefixed,
    )


def build_public_section_group_filter(group_key: str):
    normalized = normalize_section_key(group_key)
    prefixed = f"#{normalized}"
    key_filter = or_(
        SiteSection.key == normalized,
        SiteSection.key == prefixed,
        func.trim(SiteSection.key) == normalized,
        func.trim(SiteSection.key) == prefixed,
    )
    return or_(
        SiteSection.group_key == normalized,
        SiteSection.group_key == prefixed,
        func.trim(SiteSection.group_key) == normalized,
        func.trim(SiteSection.group_key) == prefixed,
        and_(SiteSection.group_key.is_(None), key_filter),
    )


def paginate_public_query(query, page: int, page_size: int):
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PageResult(total=total, page=page, page_size=page_size, items=items)


def get_active_section_roots(db: Session):
    return (
        db.query(SiteSection)
        .filter(SiteSection.is_active.is_(True), SiteSection.node_type == "section")
        .order_by(SiteSection.sort_order.asc(), SiteSection.created_at.asc(), SiteSection.id.asc())
        .all()
    )


@router.get("/home", response_model=HomePageResponse)
def get_homepage(db: Session = Depends(get_db)) -> HomePageResponse:
    """Aggregate all homepage content so the frontend can render from one request."""
    banners = (
        db.query(HeroBanner)
        .filter(HeroBanner.is_active.is_(True))
        .order_by(HeroBanner.sort_order.asc(), HeroBanner.created_at.desc())
        .all()
    )
    roots = get_active_section_roots(db)
    section_roots = [root for root in roots if root.content_source == "section"]
    section_root_keys = [root.key for root in section_roots]
    sections = apply_section_content_order(
        db.query(SiteSection).filter(
            SiteSection.is_active.is_(True),
            SiteSection.node_type == "content",
            SiteSection.group_key.in_(section_root_keys or [""]),
        ),
        SiteSection,
    ).all()
    products = (
        apply_pinned_order(
            db.query(Product).filter(Product.is_active.is_(True)),
            Product,
            "created_at",
            "id",
        )
        .limit(HOMEPAGE_PRODUCT_LIMIT)
        .all()
    )
    news = (
        apply_pinned_order(
            db.query(NewsArticle).filter(NewsArticle.is_active.is_(True)),
            NewsArticle,
            "published_at",
            "created_at",
            "id",
        )
        .limit(HOMEPAGE_NEWS_LIMIT)
        .all()
    )
    product_intro = next((root for root in roots if root.content_source == "product"), None)
    news_intro = next((root for root in roots if root.content_source == "news"), None)
    if product_intro is None:
        product_intro = (
            db.query(SiteSection)
            .filter(SiteSection.key == "product_intro", SiteSection.is_active.is_(True))
            .first()
        )
    if news_intro is None:
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
    latest_sections = {}
    for section in sections:
        group_key = normalize_section_key(section.group_key or section.key)
        if group_key in latest_sections:
            continue
        latest_sections[group_key] = section

    homepage_sections = []
    for root in section_roots:
        section = latest_sections.get(root.key)
        if not section:
            continue
        section.subtitle = root.subtitle
        homepage_sections.append(section)

    return HomePageResponse(
        banners=banners,
        sections=homepage_sections,
        products=products,
        news=news,
        product_intro=product_intro,
        news_intro=news_intro,
        footer_qr_codes=get_footer_qr_codes(db),
        footer_filing=footer_filing,
    )

@router.get("/section-groups/{group_key}", response_model=SectionArchiveResponse)
def list_public_section_group(
    group_key: str,
    page: int = 1,
    page_size: int = 9,
    db: Session = Depends(get_db),
) -> SectionArchiveResponse:
    normalized_group_key = normalize_section_key(group_key)
    root = (
        db.query(SiteSection)
        .filter(
            SiteSection.node_type == "section",
            SiteSection.content_source == "section",
            build_public_section_key_filter(normalized_group_key),
        )
        .first()
    )
    if not root:
        raise HTTPException(status_code=404, detail="Section group not found")

    query = apply_section_content_order(
        db.query(SiteSection).filter(
            SiteSection.is_active.is_(True),
            SiteSection.node_type == "content",
            or_(
                SiteSection.parent_id == root.id,
                build_public_section_group_filter(normalized_group_key),
            ),
        ),
        SiteSection,
    )
    result = paginate_public_query(query, page=page, page_size=page_size)
    return SectionArchiveResponse(
        root=SectionRead.from_orm(root),
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        items=result.items,
    )


@router.get("/sections/{section_key}", response_model=SectionRead)
def get_public_section_detail(section_key: str, db: Session = Depends(get_db)) -> SectionRead:
    section = (
        db.query(SiteSection)
        .filter(
            build_public_section_key_filter(section_key),
            SiteSection.is_active.is_(True),
            SiteSection.node_type == "content",
        )
        .first()
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.get("/products", response_model=PageResult[ProductRead])
def list_public_products(
    page: int = 1,
    page_size: int = 9,
    db: Session = Depends(get_db),
) -> PageResult[ProductRead]:
    query = apply_pinned_order(
        db.query(Product).filter(Product.is_active.is_(True)),
        Product,
        "created_at",
        "id",
    )
    return paginate_public_query(query, page=page, page_size=page_size)


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


@router.get("/news", response_model=PageResult[NewsRead])
def list_public_news(
    page: int = 1,
    page_size: int = 9,
    db: Session = Depends(get_db),
) -> PageResult[NewsRead]:
    query = apply_pinned_order(
        db.query(NewsArticle).filter(NewsArticle.is_active.is_(True)),
        NewsArticle,
        "published_at",
        "created_at",
        "id",
    )
    return paginate_public_query(query, page=page, page_size=page_size)


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








