"""Точка входа FastAPI-приложения.

Собирается приложение, подключаются обработчики ошибок, CORS и роутеры.
Авторизация/профиль — Этап 3. Каталог/статьи — Этап 4, корзина/заказ — 6–7.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .errors import register_exception_handlers
from .routers import articles, auth, categories, products, users

app = FastAPI(title="RoastRoad", version="0.1.0")

# Единый формат ошибок: {"detail": "..."} и логирование 500-х.
register_exception_handlers(app)

# CORS: только явно перечисленные origin, никакого "*" вместе с credentials.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    """Проверка, что сервер жив."""
    return {"status": "ok", "service": "RoastRoad API"}


@app.get("/api/health")
def health() -> dict:
    """Health-check для проверки работоспособности."""
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(articles.router)
