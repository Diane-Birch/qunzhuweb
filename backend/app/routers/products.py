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
from backend.app.models.product import Product
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.product import ProductCreate, ProductRead, ProductUpdate


router = APIRouter(prefix="/products", tags=["products"])


def build_product_weight(reference_time=None) -> int:
    timestamp = int((reference_time or datetime.utcnow()).timestamp())
    return max(timestamp, 1)


@router.get("", response_model=PageResult[ProductRead])
def list_products(
    page: int = 1,
    page_size: int = 12,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(Product), Product, keyword, ["name", "subtitle"])
    query = apply_pinned_order(query, Product, "created_at", "id")
    return paginate_query(query, PageParams(page=page, page_size=page_size, keyword=keyword))


@router.post("", response_model=ProductRead)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    payload.sort_order = build_product_weight()
    return create_record(db, Product, payload)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    payload.sort_order = 0 if product.sort_order == 0 else build_product_weight(product.created_at)
    return update_record(db, product, payload)


@router.post("/{product_id}/pin", response_model=ProductRead)
def pin_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.sort_order = 0
    product.pinned_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product


@router.post("/{product_id}/unpin", response_model=ProductRead)
def unpin_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.sort_order = build_product_weight(product.created_at)
    product.pinned_at = None
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_record(db, product)
    return {"message": "Product deleted"}
