"""CRUD для статей."""

import math

from sqlalchemy.orm import Session

from ..errors import NotFoundError
from ..models.article import Article


def list_articles(db: Session, skip: int = 0, limit: int = 100) -> list[Article]:
    return (
        db.query(Article)
        .filter(Article.is_published.is_(True))
        .order_by(Article.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get(db: Session, article_id: int, *, published_only: bool = False) -> Article:
    article = db.get(Article, article_id)
    if article is None or (published_only and not article.is_published):
        raise NotFoundError("Статья не найдена")
    return article


def get_and_register_view(db: Session, article_id: int) -> Article:
    """Возвращает опубликованную статью и увеличивает счётчик просмотров."""
    article = get(db, article_id, published_only=True)
    article.views += 1
    db.commit()
    db.refresh(article)
    return article


def reading_time_minutes(content: str) -> int:
    """Примерное время чтения: ~200 слов в минуту, минимум 1 минута."""
    words = len(content.split())
    return max(1, math.ceil(words / 200))


def create(db: Session, data: dict) -> Article:
    article = Article(**data)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update(db: Session, article: Article, data: dict) -> Article:
    for field, value in data.items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article


def delete(db: Session, article: Article) -> None:
    db.delete(article)
    db.commit()
