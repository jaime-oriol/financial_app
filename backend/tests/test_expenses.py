"""Tests UC-02: Add expense + UC-04: View expense history.
Valida diagramas de secuencia 2 y 4 del Solution Design.
"""


def test_create_expense_success(client, auth_header):
    """Crear gasto valido devuelve 201 con categoria."""
    response = client.post("/api/expenses", json={
        "amount": 12.50,
        "description": "Lunch at school",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "12.50"
    assert data["category_name"] == "Food"


def test_create_expense_invalid_amount(client, auth_header):
    """Amount 0 o negativo devuelve 422."""
    response = client.post("/api/expenses", json={
        "amount": -5,
        "description": "Bad expense",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)
    assert response.status_code == 422


def test_create_expense_invalid_category(client, auth_header):
    """Categoria inexistente devuelve 400."""
    response = client.post("/api/expenses", json={
        "amount": 10,
        "description": "Test",
        "expense_date": "2026-04-08",
        "category_id": 999,
    }, headers=auth_header)
    assert response.status_code == 400


def test_create_expense_unauthorized(client):
    """Sin token devuelve 403."""
    response = client.post("/api/expenses", json={
        "amount": 10,
        "description": "Test",
        "expense_date": "2026-04-08",
        "category_id": 1,
    })
    assert response.status_code == 403


def test_get_expenses_empty(client, auth_header):
    """Sin gastos devuelve lista vacia."""
    response = client.get("/api/expenses", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


def test_get_expenses_with_data(client, auth_header):
    """Listar gastos devuelve los creados, ordenados por fecha desc."""
    client.post("/api/expenses", json={
        "amount": 10,
        "description": "First",
        "expense_date": "2026-04-01",
        "category_id": 1,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 20,
        "description": "Second",
        "expense_date": "2026-04-05",
        "category_id": 2,
    }, headers=auth_header)

    response = client.get("/api/expenses", headers=auth_header)
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Second"  # mas reciente primero


def test_get_expenses_filter_by_category(client, auth_header):
    """Filtrar por categoria devuelve solo los de esa categoria."""
    client.post("/api/expenses", json={
        "amount": 10,
        "description": "Food item",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 20,
        "description": "Bus ticket",
        "expense_date": "2026-04-08",
        "category_id": 2,
    }, headers=auth_header)

    response = client.get("/api/expenses?category_id=1", headers=auth_header)
    data = response.json()
    assert len(data) == 1
    assert data[0]["category_name"] == "Food"


def test_get_expenses_filter_by_date(client, auth_header):
    """Filtrar por rango de fechas funciona correctamente."""
    client.post("/api/expenses", json={
        "amount": 10,
        "description": "March expense",
        "expense_date": "2026-03-15",
        "category_id": 1,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 20,
        "description": "April expense",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)

    response = client.get(
        "/api/expenses?start_date=2026-04-01&end_date=2026-04-30",
        headers=auth_header,
    )
    data = response.json()
    assert len(data) == 1
    assert data[0]["description"] == "April expense"
