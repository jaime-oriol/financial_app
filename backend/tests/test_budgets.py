"""Tests UC-03: Create monthly budget.
Valida diagrama de secuencia 3 del Solution Design.
"""


def test_create_budget_success(client, auth_header):
    """Crear presupuesto valido devuelve 201 con progreso 0%."""
    response = client.post("/api/budgets", json={
        "category_id": 1,
        "limit_amount": 100,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["limit_amount"] == "100.00"
    assert data["progress"] == 0.0
    assert data["category_name"] == "Food"


def test_create_budget_duplicate(client, auth_header):
    """Presupuesto duplicado para misma categoria/mes devuelve 400."""
    budget_data = {
        "category_id": 1,
        "limit_amount": 100,
        "month": 4,
        "year": 2026,
    }
    client.post("/api/budgets", json=budget_data, headers=auth_header)
    response = client.post("/api/budgets", json=budget_data, headers=auth_header)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_budget_invalid_amount(client, auth_header):
    """Amount 0 o negativo devuelve 422."""
    response = client.post("/api/budgets", json={
        "category_id": 1,
        "limit_amount": 0,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)
    assert response.status_code == 422


def test_budget_tracks_spending(client, auth_header):
    """El progreso del presupuesto refleja los gastos reales."""
    # Crear presupuesto de $100 para Food en abril 2026
    client.post("/api/budgets", json={
        "category_id": 1,
        "limit_amount": 100,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)

    # Gastar $30 en Food en abril
    client.post("/api/expenses", json={
        "amount": 30,
        "description": "Groceries",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)

    # Verificar progreso
    response = client.get("/api/budgets?month=4&year=2026", headers=auth_header)
    data = response.json()
    assert len(data) == 1
    assert data[0]["spent"] == "30.00"
    assert data[0]["progress"] == 30.0


def test_get_budgets_empty(client, auth_header):
    """Sin presupuestos devuelve lista vacia."""
    response = client.get("/api/budgets?month=4&year=2026", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_budget(client, auth_header):
    """Eliminar presupuesto y verificar que no aparece."""
    create = client.post("/api/budgets", json={
        "category_id": 1, "limit_amount": 100, "month": 4, "year": 2026,
    }, headers=auth_header)
    budget_id = create.json()["budget_id"]

    response = client.delete(f"/api/budgets/{budget_id}", headers=auth_header)
    assert response.status_code == 204

    listed = client.get("/api/budgets?month=4&year=2026", headers=auth_header).json()
    assert listed == []


def test_delete_missing_budget(client, auth_header):
    """Eliminar budget inexistente devuelve 404."""
    response = client.delete("/api/budgets/9999", headers=auth_header)
    assert response.status_code == 404
