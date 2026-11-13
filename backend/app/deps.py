"""Зависимости FastAPI: сессия БД и проверка прав доступа."""

from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models.user import Role, User
from .security import verify_token

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Отдаёт сессию БД и гарантированно закрывает её после запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Возвращает текущего пользователя по Bearer-токену или 401.

    verify_token сам поднимает HTTPException(401) на невалидном/просроченном
    токене, поэтому здесь обрабатываем только случай «пользователь не найден».
    """
    user_id = verify_token(credentials.credentials)

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Разрешает доступ только администраторам, иначе 403."""
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )
    return current_user
