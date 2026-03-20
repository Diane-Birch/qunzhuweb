from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.content import (
    apply_keyword_filter,
    create_record,
    delete_record,
    paginate,
    update_record,
)
from backend.app.deps import get_current_admin
from backend.app.models.news import NewsArticle
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.news import NewsCreate, NewsRead, NewsUpdate


router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=PageResult[NewsRead])
def list_news(
    page: int = 1,
    page_size: int = 10,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(NewsArticle), NewsArticle, keyword, ["title", "summary"])
    return paginate(query, PageParams(page=page, page_size=page_size, keyword=keyword), NewsArticle, "sort_order")


@router.post("", response_model=NewsRead)
def create_news(
    payload: NewsCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
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
    return update_record(db, article, payload)


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
