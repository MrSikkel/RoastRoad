"""CRUD для категорий."""

from sqlalchemy.orm import Session

from ..models.category import Category


def list_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.id).all()
