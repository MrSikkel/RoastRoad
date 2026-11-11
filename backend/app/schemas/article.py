"""Схемы статьи."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArticleBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    short_description: str = Field(min_length=1)
    content: str = Field(min_length=1)
    images: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class ArticleCreate(ArticleBase):
    # author_id проставляется в роутере из текущего пользователя (админа).
    pass


class ArticleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    short_description: str | None = Field(default=None, min_length=1)
    content: str | None = Field(default=None, min_length=1)
    images: list[str] | None = None
    tags: list[str] | None = None
    is_published: bool | None = None


class ArticleOut(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    views: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ArticleDetailOut(ArticleOut):
    """Сводный ответ для страницы статьи: имя автора и время чтения."""

    author_name: str
    reading_time_minutes: int
