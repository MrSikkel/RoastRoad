"""Тесты каталога (категории, товары) и статей."""

from decimal import Decimal

import pytest

from app.models import Article, Category, Product, Role, User
from app.security import hash_password


@pytest.fixture()
def seed(db_session):
    admin = User(
        email="admin@x.com",
        password_hash=hash_password("admin123"),
        role=Role.admin,
    )
    author = User(
        email="author@x.com",
        password_hash=hash_password("author123"),
        first_name="Оксана",
        last_name="Денисова",
    )
    db_session.add_all([admin, author])
    db_session.flush()

    coffee = Category(name="Кофе", slug="coffee")
    tea = Category(name="Чай", slug="tea")
    db_session.add_all([coffee, tea])
    db_session.flush()

    product = Product(
        name="Натти",
        short_description="орехи и нуга",
        description="Плотный кофе со вкусом жареных орехов",
        price=Decimal("899.00"),
        category_id=coffee.id,
        images=["/media/products/coffepack1.png"],
        specifications={"type": "Для эспрессо"},
    )
    article = Article(
        name="Основные правила темперовки",
        short_description="Как сделать кофейную таблетку",
        content="Темперовка — прессование молотого кофе перед эспрессо.",
        author_id=author.id,
        images=["/media/articles/articleback1.png"],
        tags=["#Обучение"],
        is_published=True,
    )
    db_session.add_all([product, article])
    db_session.commit()
    return {"coffee": coffee, "tea": tea, "product": product, "article": article}


# --- Категории ---

def test_list_categories(client, seed):
    r = client.get("/api/categories")
    assert r.status_code == 200
    slugs = [c["slug"] for c in r.json()]
    assert "coffee" in slugs
    assert "tea" in slugs


# --- Товары ---

def test_list_products_returns_array(client, seed):
    r = client.get("/api/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 1
    assert "X-Total-Count" in r.headers


def test_product_filter_by_category(client, seed):
    assert len(client.get("/api/products?category=coffee").json()) == 1
    assert client.get("/api/products?category=tea").json() == []


def test_product_search(client, seed):
    r = client.get("/api/products?q=Натти")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "Натти"


def test_get_product_with_category(client, seed):
    r = client.get(f"/api/products/{seed['product'].id}")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Натти"
    assert body["short_description"] == "орехи и нуга"
    assert body["category"]["slug"] == "coffee"


def test_get_product_404(client):
    assert client.get("/api/products/999").status_code == 404


def test_create_product_forbidden_for_user(client, seed):
    client.post("/api/auth/register", json={"email": "u@x.com", "password": "pass123"})
    token = client.post(
        "/api/auth/login", json={"email": "u@x.com", "password": "pass123"}
    ).json()["access_token"]
    r = client.post(
        "/api/products",
        json={"name": "X", "price": "100", "category_id": seed["coffee"].id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403


def test_create_product_as_admin(client, seed):
    token = client.post(
        "/api/auth/login", json={"email": "admin@x.com", "password": "admin123"}
    ).json()["access_token"]
    r = client.post(
        "/api/products",
        json={"name": "Новый кофе", "price": "100", "category_id": seed["coffee"].id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    assert r.json()["name"] == "Новый кофе"


# --- Статьи ---

def test_list_articles(client, seed):
    r = client.get("/api/articles")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_article_increments_views_and_author(client, seed):
    r = client.get(f"/api/articles/{seed['article'].id}")
    assert r.status_code == 200
    body = r.json()
    assert body["author_name"] == "Оксана Денисова"
    assert body["reading_time_minutes"] >= 1
    assert body["views"] == 1

    r2 = client.get(f"/api/articles/{seed['article'].id}")
    assert r2.json()["views"] == 2


def test_create_article_requires_admin(client, seed):
    client.post("/api/auth/register", json={"email": "u@x.com", "password": "pass123"})
    token = client.post(
        "/api/auth/login", json={"email": "u@x.com", "password": "pass123"}
    ).json()["access_token"]
    r = client.post(
        "/api/articles",
        json={"name": "A", "short_description": "s", "content": "c"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403
