"""Статьи блога, комментарии и лайки комментариев."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    short_description: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    images: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    views: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    author: Mapped[User] = relationship(back_populates="articles")
    comments: Mapped[list[ArticleComment]] = relationship(back_populates="article")


class ArticleComment(Base):
    __tablename__ = "article_comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    article: Mapped[Article] = relationship(back_populates="comments")
    user: Mapped[User] = relationship(back_populates="comments")
    likes: Mapped[list[CommentLike]] = relationship(
        back_populates="comment", cascade="all, delete-orphan"
    )


class CommentLike(Base):
    __tablename__ = "comment_likes"
    __table_args__ = (UniqueConstraint("comment_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("article_comments.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    comment: Mapped[ArticleComment] = relationship(back_populates="likes")
    user: Mapped[User] = relationship(back_populates="comment_likes")
