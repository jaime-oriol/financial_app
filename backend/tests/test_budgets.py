"""Tests UC-03: Create monthly budget.
Valida diagrama de secuencia 3 del Solution Design.
"""


def test_create_budget_success(client, auth_header):
    """Crear presupuesto valido devuelve 201 con progreso 0%."""
    response = client.post("/budgets", json={
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
    client.post("/budgets", json=budget_data, headers=auth_header)
    response = client.post("/budgets", json=budget_data, headers=auth_header)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_budget_invalid_amount(client, auth_header):
    """Amount 0 o negativo devuelve 422."""
    response = client.post("/budgets", json={
        "category_id": 1,
        "limit_amount": 0,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)
    assert response.status_code == 422


def test_budget_tracks_spending(client, auth_header):
    """El progreso del presupuesto refleja los gastos reales."""
    # Crear presupuesto de $100 para Food en abril 2026
    client.post("/budgets", json={
        "category_id": 1,
        "limit_amount": 100,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)

    # Gastar $30 en Food en abril
    client.post("/expenses", json={
        "amount": 30,
        "description": "Groceries",
        "expense_date": "2026-04-08",
        "category_id": 1,
    }, headers=auth_header)

    # Verificar progreso
    response = client.get("/budgets?month=4&year=2026", headers=auth_header)
    data = response.json()
    assert len(data) == 1
    assert data[0]["spent"] == "30.00"
    assert data[0]["progress"] == 30.0


def test_get_budgets_empty(client, auth_header):
    """Sin presupuestos devuelve lista vacia."""
    response = client.get("/budgets?month=4&year=2026", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []
