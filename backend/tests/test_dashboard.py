"""Tests UC-05: View dashboard / simple analytics.
Valida diagrama de secuencia 5 del Solution Design.
"""


def test_dashboard_empty(client, auth_header):
    """Dashboard sin datos devuelve listas vacias (placeholder state)."""
    response = client.get("/api/dashboard", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["spending_by_category"] == []
    assert data["budgets"] == []
    assert data["recent_transactions"] == []


def test_dashboard_with_data(client, auth_header):
    """Dashboard con gastos y presupuestos devuelve resumen correcto."""
    # Crear presupuesto
    client.post("/api/budgets", json={
        "category_id": 1,
        "limit_amount": 200,
        "month": 4,
        "year": 2026,
    }, headers=auth_header)

    # Crear gastos en abril 2026
    client.post("/api/expenses", json={
        "amount": 25,
        "description": "Lunch",
        "expense_date": "2026-04-05",
        "category_id": 1,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 15,
        "description": "Snack",
        "expense_date": "2026-04-07",
        "category_id": 1,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 30,
        "description": "Movie",
        "expense_date": "2026-04-06",
        "category_id": 3,
    }, headers=auth_header)

    response = client.get("/api/dashboard", headers=auth_header)
    data = response.json()

    # Spending by category: Food=$40, Entertainment=$30
    assert len(data["spending_by_category"]) == 2
    food = next(s for s in data["spending_by_category"] if s["category_name"] == "Food")
    assert food["total"] == "40.00"

    # Budget progress: Food $40/$200 = 20%
    assert len(data["budgets"]) == 1
    assert data["budgets"][0]["progress"] == 20.0

    # Recent transactions: 3 gastos
    assert len(data["recent_transactions"]) == 3


def test_dashboard_unauthorized(client):
    """Dashboard sin token devuelve 403."""
    response = client.get("/api/dashboard")
    assert response.status_code == 403
