"""Тесты адресов пользователя."""


def _auth(client, email="a@x.com"):
    client.post("/api/auth/register", json={"email": email, "password": "pass123"})
    token = client.post(
        "/api/auth/login", json={"email": email, "password": "pass123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_address_crud(client):
    headers = _auth(client)
    data = {"city": "Томск", "street": "Советская", "house": "10", "apartment": "5"}

    # Создание — первый адрес автоматически становится дефолтным.
    r = client.post("/api/users/addresses", json=data, headers=headers)
    assert r.status_code == 201
    addr = r.json()
    assert addr["city"] == "Томск"
    assert addr["is_default"] is True
    addr_id = addr["id"]

    # Список.
    r = client.get("/api/users/addresses", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Обновление.
    r = client.put(
        f"/api/users/addresses/{addr_id}", json={"city": "Новосибирск"}, headers=headers
    )
    assert r.status_code == 200
    assert r.json()["city"] == "Новосибирск"

    # Удаление.
    r = client.delete(f"/api/users/addresses/{addr_id}", headers=headers)
    assert r.status_code == 204
    assert client.get("/api/users/addresses", headers=headers).json() == []


def test_address_not_accessible_to_other_user(client):
    headers_a = _auth(client, "a@x.com")
    headers_b = _auth(client, "b@x.com")

    r = client.post(
        "/api/users/addresses",
        json={"city": "Томск", "street": "Советская", "house": "10"},
        headers=headers_a,
    )
    addr_id = r.json()["id"]

    # Пользователь B не может менять адрес пользователя A.
    r = client.put(
        f"/api/users/addresses/{addr_id}", json={"city": "X"}, headers=headers_b
    )
    assert r.status_code == 404
