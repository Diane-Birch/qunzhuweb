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
from backend.app.models.product import Product
from backend.app.models.user import AdminUser
from backend.app.schemas.common import PageParams, PageResult
from backend.app.schemas.product import ProductCreate, ProductRead, ProductUpdate


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PageResult[ProductRead])
def list_products(
    page: int = 1,
    page_size: int = 12,
    keyword: str = None,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    query = apply_keyword_filter(db.query(Product), Product, keyword, ["name", "subtitle"])
    return paginate(query, PageParams(page=page, page_size=page_size, keyword=keyword), Product, "sort_order")


@router.post("", response_model=ProductRead)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
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
    return update_record(db, product, payload)


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
