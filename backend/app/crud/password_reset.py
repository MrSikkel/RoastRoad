"""CRUD для токенов сброса пароля."""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..errors import ConflictError, NotFoundError
from ..models.password_reset import PasswordResetToken

RESET_TOKEN_TTL = timedelta(hours=1)


def _utcnow() -> datetime:
    """Наивное UTC-время (как в колонках DateTime без timezone)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_token(db: Session, user_id: int) -> PasswordResetToken:
    reset = PasswordResetToken(
        user_id=user_id,
        token=secrets.token_urlsafe(32),
        expires_at=_utcnow() + RESET_TOKEN_TTL,
    )
    db.add(reset)
    db.commit()
    db.refresh(reset)
    return reset


def get_valid_token(db: Session, token: str) -> PasswordResetToken:
    reset = (
        db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    )
    if reset is None or reset.used:
        raise NotFoundError("Токен сброса не найден или уже использован")
    if reset.expires_at < _utcnow():
        raise ConflictError("Срок действия токена истёк")
    return reset


def mark_used(db: Session, reset: PasswordResetToken) -> None:
    reset.used = True
    db.commit()
