"""Конфигурация приложения на основе pydantic-settings.

Все секреты и параметры окружения читаются только отсюда. Другие модули
импортируют объект `settings` и не содержат хардкода (никаких
"my-secret-key" или зашитых путей к БД).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта, загружаемые из переменных окружения и файла .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Без значения по умолчанию. Если SECRET_KEY не задан ни в окружении,
    # ни в .env, при создании объекта Settings произойдёт ValidationError —
    # приложение упадёт на старте, а не запустится с известным ключом.
    secret_key: str

    database_url: str = "sqlite:///./roastroad.db"
    access_token_minutes: int = 30

    # Список разрешённых origin для CORS. Передаётся JSON-массивом, напр.:
    #   CORS_ORIGINS='["http://localhost:3000"]'
    # По умолчанию пусто: фронт раздаётся с того же origin, CORS не нужен.
    # Звёздочка "*" вместе с allow_credentials=True недопустима.
    cors_origins: list[str] = []


# Создаётся в момент импорта модуля. Именно здесь происходит проверка
# обязательного SECRET_KEY.
settings = Settings()
