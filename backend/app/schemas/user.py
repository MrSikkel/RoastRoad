"""Схемы пользователя."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from ..models.user import Role
from .common import Name, Password, Phone, validate_password_strength


class UserRegister(BaseModel):
    """Регистрация: имена и телефон необязательны."""

    email: EmailStr
    password: Password
    first_name: Name | None = None
    last_name: Name | None = None
    patronymic: Name | None = None
    phone: Phone | None = None

    @field_validator("password")
    @classmethod
    def _check_password(cls, value: str) -> str:
        return validate_password_strength(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Профиль пользователя. Поля имён не имеют min_length — пустая строка
    в БД не должна ломать ответ."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    phone: str | None
    role: Role
    registration_date: datetime


class UserUpdate(BaseModel):
    """Обновление профиля: все поля необязательны (exclude_unset на этапе CRUD)."""

    email: EmailStr | None = None
    first_name: Name | None = None
    last_name: Name | None = None
    patronymic: Name | None = None
    phone: Phone | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePassword(BaseModel):
    current_password: str
    new_password: Password

    @field_validator("new_password")
    @classmethod
    def _check_password(cls, value: str) -> str:
        return validate_password_strength(value)


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: Password

    @field_validator("new_password")
    @classmethod
    def _check_password(cls, value: str) -> str:
        return validate_password_strength(value)
