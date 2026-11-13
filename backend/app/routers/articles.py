"""Роутер статей."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_db, require_admin
from ..models.user import User

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("", response_model=list[schemas.ArticleOut])
def list_articles(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.article.list_articles(db, skip=skip, limit=limit)


@router.get("/{article_id}", response_model=schemas.ArticleDetailOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.article.get_and_register_view(db, article_id)
    author = article.author
    author_name = " ".join(filter(None, [author.first_name, author.last_name])) or author.email
    return {
        **schemas.ArticleOut.model_validate(article).model_dump(),
        "author_name": author_name,
        "reading_time_minutes": crud.article.reading_time_minutes(article.content),
    }


@router.post("", response_model=schemas.ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    data = payload.model_dump()
    data["author_id"] = current_user.id
    return crud.article.create(db, data)


@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    article_id: int,
    payload: schemas.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    article = crud.article.get(db, article_id)
    return crud.article.update(db, article, payload.model_dump(exclude_unset=True))


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    article = crud.article.get(db, article_id)
    crud.article.delete(db, article)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
