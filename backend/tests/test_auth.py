"""Тесты авторизации и профиля."""


def _register(client, email="a@x.com", password="pass123"):
    return client.post("/api/auth/register", json={"email": email, "password": password})


def test_register(client):
    r = _register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "a@x.com"
    assert body["first_name"] is None
    assert body["last_name"] is None


def test_register_duplicate_email(client):
    assert _register(client).status_code == 201
    r = _register(client)
    assert r.status_code == 409
    assert isinstance(r.json()["detail"], str)


def test_login_and_me(client):
    _register(client)
    r = client.post("/api/auth/login", json={"email": "a@x.com", "password": "pass123"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    me = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "a@x.com"


def test_login_json_alias(client):
    _register(client)
    r = client.post(
        "/api/auth/login-json", json={"email": "a@x.com", "password": "pass123"}
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    _register(client)
    r = client.post(
        "/api/auth/login", json={"email": "a@x.com", "password": "wrongpass1"}
    )
    assert r.status_code == 401


def test_me_invalid_token(client):
    r = client.get("/api/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401


def test_me_no_token(client):
    # HTTPBearer без заголовка возвращает 403, а не 401.
    r = client.get("/api/users/me")
    assert r.status_code == 403


def test_change_password(client):
    _register(client)
    token = client.post(
        "/api/auth/login", json={"email": "a@x.com", "password": "pass123"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/auth/change-password",
        json={"current_password": "pass123", "new_password": "newpass123"},
        headers=headers,
    )
    assert r.status_code == 200

    assert (
        client.post(
            "/api/auth/login", json={"email": "a@x.com", "password": "pass123"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/auth/login", json={"email": "a@x.com", "password": "newpass123"}
        ).status_code
        == 200
    )
