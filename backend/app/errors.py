"""Глобальные обработчики ошибок FastAPI и собственные исключения.

Единый формат ошибок: всегда {"detail": <строка>}. Внутренности сервера
(тексты SQL-ошибок, трейсбеки) наружу не отдаются — они только логируются.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Базовое бизнес-исключение с HTTP-статусом и текстом."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    """Ресурс не найден (404)."""

    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(404, detail)


class ConflictError(AppError):
    """Конфликт данных, например дубликат (409)."""

    def __init__(self, detail: str = "Конфликт данных") -> None:
        super().__init__(409, detail)


def _format_validation_error(error: dict) -> str:
    """Превращает первую ошибку валидации в человекочитаемую строку."""
    location = ".".join(str(part) for part in error.get("loc", ()) if part != "body")
    message = error.get("msg", "Invalid value")
    return f"{location}: {message}" if location else message


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует глобальные обработчики ошибок на экземпляре приложения."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        first_error = errors[0] if errors else {"msg": "Validation error"}
        return JSONResponse(
            status_code=422,
            content={"detail": _format_validation_error(first_error)},
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        # Полный трейсбек пишем в лог, клиенту отдаём только общую фразу.
        logger.error(
            "Unhandled exception",
            exc_info=(type(exc), exc, exc.__traceback__),
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
