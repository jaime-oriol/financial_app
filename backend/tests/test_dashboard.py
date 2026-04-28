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


def test_dashboard_streak_real_from_expenses(client, auth_header):
    """Streak se calcula desde expense_date — dias consecutivos terminando hoy."""
    from datetime import date, timedelta
    today = date.today()
    # Hoy + ayer + anteayer = streak 3
    for i in range(3):
        client.post("/api/expenses", json={
            "amount": 5, "description": f"day-{i}",
            "expense_date": (today - timedelta(days=i)).isoformat(),
            "category_id": 1,
        }, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    assert response.json()["streak"] == 3


def test_dashboard_streak_breaks_on_gap(client, auth_header):
    """Si falta un dia, streak se rompe y solo cuenta los recientes."""
    from datetime import date, timedelta
    today = date.today()
    client.post("/api/expenses", json={
        "amount": 5, "description": "today",
        "expense_date": today.isoformat(), "category_id": 1,
    }, headers=auth_header)
    # Salto: gasto hace 3 dias (no consecutivo con hoy)
    client.post("/api/expenses", json={
        "amount": 5, "description": "old",
        "expense_date": (today - timedelta(days=3)).isoformat(),
        "category_id": 1,
    }, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    assert response.json()["streak"] == 1


def test_dashboard_daily_spending_has_seven_days(client, auth_header):
    """daily_spending devuelve siempre 7 dias (rellena con 0 si no hay gasto)."""
    response = client.get("/api/dashboard", headers=auth_header)
    daily = response.json()["daily_spending"]
    assert len(daily) == 7


def test_dashboard_xp_aggregates_attempts(client, auth_header):
    """total_xp = suma de xp_earned de todos los intentos."""
    client.post("/api/challenges/1/attempt",
                json={"payload": {"score": 2, "total": 3}}, headers=auth_header)
    client.post("/api/challenges/2/attempt",
                json={"payload": {"choice_idx": 1}}, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    data = response.json()
    assert data["total_xp"] == 45  # 20 + 25
    assert data["challenges_done"] == 2


def test_dashboard_achievements_returned(client, auth_header):
    """Achievements vienen siempre — earned se calcula segun datos del user."""
    response = client.get("/api/dashboard", headers=auth_header)
    achievements = response.json()["achievements"]
    ids = sorted(a["id"] for a in achievements)
    assert ids == [
        "budget_pro", "first_saver", "goal_crusher", "hot_streak", "quiz_master"
    ]
    # Sin datos: ninguno earned
    assert all(a["earned"] is False for a in achievements)


def test_achievement_first_saver(client, auth_header):
    """First Saver se desbloquea al hacer una contribucion > 0 a un goal."""
    create = client.post("/api/goals", json={
        "name": "Bike", "target_amount": 100,
    }, headers=auth_header).json()
    client.post(f"/api/goals/{create['goal_id']}/contribute",
                json={"amount": 10}, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    earned = {a["id"]: a["earned"] for a in response.json()["achievements"]}
    assert earned["first_saver"] is True


def test_achievement_quiz_master(client, auth_header):
    """Quiz Master se desbloquea con score perfecto en el quiz."""
    client.post("/api/challenges/1/attempt",
                json={"payload": {"score": 3, "total": 3}}, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    earned = {a["id"]: a["earned"] for a in response.json()["achievements"]}
    assert earned["quiz_master"] is True


def test_achievement_goal_crusher(client, auth_header):
    """Goal Crusher se desbloquea al completar una meta (saved >= target)."""
    create = client.post("/api/goals", json={
        "name": "Fast", "target_amount": 50,
    }, headers=auth_header).json()
    client.post(f"/api/goals/{create['goal_id']}/contribute",
                json={"amount": 50}, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    earned = {a["id"]: a["earned"] for a in response.json()["achievements"]}
    assert earned["goal_crusher"] is True


def test_achievement_budget_pro(client, auth_header):
    """Budget Pro: presupuesto + al menos un gasto."""
    client.post("/api/budgets", json={
        "category_id": 1, "limit_amount": 100, "month": 4, "year": 2026,
    }, headers=auth_header)
    client.post("/api/expenses", json={
        "amount": 5, "description": "x",
        "expense_date": "2026-04-08", "category_id": 1,
    }, headers=auth_header)
    response = client.get("/api/dashboard", headers=auth_header)
    earned = {a["id"]: a["earned"] for a in response.json()["achievements"]}
    assert earned["budget_pro"] is True
