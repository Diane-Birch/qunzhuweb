from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.content import (
    apply_keyword_filter,
    apply_pinned_order,
    create_record,
    delete_record,
    paginate_query,
    update_record,
)
from backend.app.deps import get_current_admin
from backend.app.models.news import NewsArticle
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.news import NewsCreate, NewsRead, NewsUpdate


router = APIRouter(prefix="/news", tags=["news"])


def build_news_weight(reference_time=None) -> int:
    timestamp = int((reference_time or datetime.utcnow()).timestamp())
    return max(timestamp, 1)


@router.get("", response_model=PageResult[NewsRead])
def list_news(
    page: int = 1,
    page_size: int = 10,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(NewsArticle), NewsArticle, keyword, ["title", "summary"])
    query = apply_pinned_order(query, NewsArticle, "published_at", "created_at", "id")
    return paginate_query(query, PageParams(page=page, page_size=page_size, keyword=keyword))


@router.post("", response_model=NewsRead)
def create_news(
    payload: NewsCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    payload.sort_order = build_news_weight(payload.published_at)
    return create_record(db, NewsArticle, payload)


@router.put("/{news_id}", response_model=NewsRead)
def update_news(
    news_id: int,
    payload: NewsUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    payload.sort_order = 0 if article.sort_order == 0 else build_news_weight(payload.published_at)
    return update_record(db, article, payload)


@router.post("/{news_id}/pin", response_model=NewsRead)
def pin_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")

    article.sort_order = 0
    article.pinned_at = datetime.utcnow()
    db.commit()
    db.refresh(article)
    return article


@router.post("/{news_id}/unpin", response_model=NewsRead)
def unpin_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")

    article.sort_order = build_news_weight(article.published_at)
    article.pinned_at = None
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{news_id}")
def remove_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    delete_record(db, article)
    return {"message": "News deleted"}
