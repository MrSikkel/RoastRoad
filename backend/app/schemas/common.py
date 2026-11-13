"""Общие переиспользуемые типы и валидаторы."""

from typing import Annotated

from pydantic import StringConstraints

# Имя/фамилия/отчество: только буквы, пробелы и дефисы; обрезается по краям.
Name = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$",
    ),
]

# Телефон в международном формате.
Phone = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=20,
        pattern=r"^\+?[1-9]\d{1,14}$",
    ),
]

# Пароль: от 6 символов. argon2 не имеет лимита в 72 байта, как bcrypt.
Password = Annotated[str, StringConstraints(min_length=6, max_length=128)]


def validate_password_strength(value: str) -> str:
    """Пароль должен содержать хотя бы одну букву и одну цифру."""
    if not any(ch.isdigit() for ch in value):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")
    if not any(ch.isalpha() for ch in value):
        raise ValueError("Пароль должен содержать хотя бы одну букву")
    return value
