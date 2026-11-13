"""Роутер категорий."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.category.list_categories(db)
