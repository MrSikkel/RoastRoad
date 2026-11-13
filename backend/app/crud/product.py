"""CRUD для товаров."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..errors import NotFoundError
from ..models.category import Category
from ..models.product import Product


def list_products(
    db: Session,
    category: str | None = None,
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[Product], int]:
    query = db.query(Product).filter(Product.is_active.is_(True))
    if category:
        query = query.join(Category).filter(Category.slug == category)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Product.name.ilike(like),
                Product.short_description.ilike(like),
                Product.description.ilike(like),
            )
        )
    total = query.count()
    items = query.order_by(Product.id).offset(skip).limit(limit).all()
    return items, total


def get(db: Session, product_id: int, *, active_only: bool = False) -> Product:
    product = db.get(Product, product_id)
    if product is None or (active_only and not product.is_active):
        raise NotFoundError("Товар не найден")
    return product


def create(db: Session, data: dict) -> Product:
    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product: Product, data: dict) -> Product:
    for field, value in data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
