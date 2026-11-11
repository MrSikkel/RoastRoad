"""CRUD для пользователей."""

from sqlalchemy.orm import Session

from ..errors import ConflictError, NotFoundError
from ..models.user import User
from ..security import hash_password


def get_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError("Пользователь не найден")
    return user


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def create(db: Session, email: str, password: str, **kwargs) -> User:
    email = email.lower()
    if get_by_email(db, email) is not None:
        raise ConflictError("Пользователь с таким email уже существует")
    user = User(email=email, password_hash=hash_password(password), **kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, data: dict) -> User:
    """Обновляет пользователя. `data` содержит только явно переданные поля."""
    if "email" in data:
        email = data.pop("email")
        if email is not None:
            email = email.lower()
            existing = get_by_email(db, email)
            if existing is not None and existing.id != user.id:
                raise ConflictError("Пользователь с таким email уже существует")
            user.email = email
        # email=None игнорируем — email нельзя очистить.

    for field, value in data.items():
        setattr(user, field, value)  # None тоже применяется (сброс поля)

    db.commit()
    db.refresh(user)
    return user


def set_password(db: Session, user: User, new_password: str) -> None:
    user.password_hash = hash_password(new_password)
    db.commit()
