"""Пользователь и его роль."""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Role(enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    patronymic: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    addresses: Mapped[list[UserAddress]] = relationship(back_populates="user")
    articles: Mapped[list[Article]] = relationship(back_populates="author")
    comments: Mapped[list[ArticleComment]] = relationship(back_populates="user")
    comment_likes: Mapped[list[CommentLike]] = relationship(back_populates="user")
    cart: Mapped[Cart | None] = relationship(back_populates="user", uselist=False)
    orders: Mapped[list[Order]] = relationship(back_populates="user")
