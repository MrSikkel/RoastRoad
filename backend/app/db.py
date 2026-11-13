"""Настройка SQLAlchemy: engine, SessionLocal и декларативный Base.

DATABASE_URL берётся из настроек (config.settings). Для SQLite дополнительно
включается PRAGMA foreign_keys=ON, потому что SQLite по умолчанию не проверяет
внешние ключи.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""


_is_sqlite = settings.database_url.startswith("sqlite")

engine = create_engine(
    settings.database_url,
    # check_same_thread нужен только для SQLite: сессии отдаются из разных
    # потоков FastAPI, а SQLite-соединение привязано к одному потоку.
    connect_args={"check_same_thread": False} if _is_sqlite else {},
)


if _is_sqlite:
    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
        """Включает проверку внешних ключей для каждого нового соединения."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
