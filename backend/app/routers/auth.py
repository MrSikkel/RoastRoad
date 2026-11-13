"""Роутер авторизации."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_current_user, get_db
from ..models.user import User
from ..security import create_access_token, verify_password

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)) -> User:
    return crud.user.create(
        db,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        patronymic=payload.patronymic,
        phone=payload.phone,
    )


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)) -> schemas.Token:
    user = crud.user.get_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    return schemas.Token(access_token=create_access_token(user.id))


# Алиас для текущего фронта (auth.js использует /auth/login-json). Уберём на Этапе 5.
@router.post("/login-json", response_model=schemas.Token)
def login_json(
    payload: schemas.UserLogin, db: Session = Depends(get_db)
) -> schemas.Token:
    return login(payload, db)


@router.post("/change-password")
def change_password(
    payload: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текущий пароль указан неверно",
        )
    crud.user.set_password(db, current_user, payload.new_password)
    return {"detail": "Пароль успешно изменён"}


@router.post("/forgot-password")
def forgot_password(
    payload: schemas.ForgotPassword, db: Session = Depends(get_db)
) -> dict:
    user = crud.user.get_by_email(db, payload.email)
    if user is not None:
        reset = crud.password_reset.create_token(db, user.id)
        # Пока письмо пишем в лог (SMTP подключим на Этапе 9).
        logger.info(
            "Ссылка для сброса пароля пользователя %s: /reset?token=%s",
            user.email,
            reset.token,
        )
    # Отвечаем одинаково, чтобы не раскрывать существование email.
    return {"detail": "Если такой email существует, инструкция по сбросу отправлена"}


@router.post("/reset-password")
def reset_password(
    payload: schemas.ResetPassword, db: Session = Depends(get_db)
) -> dict:
    reset = crud.password_reset.get_valid_token(db, payload.token)
    user = crud.user.get_by_id(db, reset.user_id)
    crud.user.set_password(db, user, payload.new_password)
    crud.password_reset.mark_used(db, reset)
    return {"detail": "Пароль успешно сброшен"}
