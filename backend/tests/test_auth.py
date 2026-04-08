"""Tests UC-01: Register account.
Valida el diagrama de secuencia 1 del Solution Design:
- Campos incompletos -> 422
- Email ya registrado -> 400
- Password debil -> 422
- Registro exitoso -> 201 + token
- Login correcto -> 200 + token
- Login incorrecto -> 401
"""


def test_register_success(client):
    """Registro exitoso devuelve 201 con token y user_id."""
    response = client.post("/auth/register", json={
        "name": "Alex",
        "surname": "Johnson",
        "birthdate": "2009-03-20",
        "email": "alex@example.com",
        "password": "strongpass123",
    })
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert "user_id" in data


def test_register_duplicate_email(client):
    """Email ya registrado devuelve 400."""
    user_data = {
        "name": "Alex",
        "surname": "Johnson",
        "birthdate": "2009-03-20",
        "email": "duplicate@example.com",
        "password": "strongpass123",
    }
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


def test_register_missing_fields(client):
    """Campos incompletos devuelve 422."""
    response = client.post("/auth/register", json={"name": "Alex"})
    assert response.status_code == 422


def test_register_weak_password(client):
    """Password menor a 6 caracteres devuelve 422."""
    response = client.post("/auth/register", json={
        "name": "Alex",
        "surname": "Johnson",
        "birthdate": "2009-03-20",
        "email": "alex@example.com",
        "password": "123",
    })
    assert response.status_code == 422


def test_login_success(client):
    """Login correcto devuelve token."""
    client.post("/auth/register", json={
        "name": "Alex",
        "surname": "Johnson",
        "birthdate": "2009-03-20",
        "email": "login@example.com",
        "password": "strongpass123",
    })
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "strongpass123",
    })
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_wrong_password(client):
    """Password incorrecta devuelve 401."""
    client.post("/auth/register", json={
        "name": "Alex",
        "surname": "Johnson",
        "birthdate": "2009-03-20",
        "email": "wrong@example.com",
        "password": "strongpass123",
    })
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "badpass",
    })
    assert response.status_code == 401
