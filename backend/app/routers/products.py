"""Роутер товаров."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_db, require_admin
from ..models.user import User

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[schemas.ProductOut])
def list_products(
    response: Response,
    category: str | None = None,
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items, total = crud.product.list_products(
        db, category=category, q=q, skip=skip, limit=limit
    )
    response.headers["X-Total-Count"] = str(total)
    return items


@router.get("/{product_id}", response_model=schemas.ProductDetailOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.product.get(db, product_id, active_only=True)


@router.post("", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.product.create(db, payload.model_dump())


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = crud.product.get(db, product_id)
    return crud.product.update(db, product, payload.model_dump(exclude_unset=True))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = crud.product.get(db, product_id)
    crud.product.delete(db, product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
