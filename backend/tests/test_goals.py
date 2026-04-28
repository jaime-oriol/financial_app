"""Tests Goals: CRUD + contribute (transactional, todo desde BD)."""


def test_create_goal_success(client, auth_header):
    """Crear meta valida devuelve 201 con saved_amount=0 y progress=0."""
    response = client.post("/api/goals", json={
        "name": "Headphones",
        "target_amount": 150,
        "deadline": "2026-12-31",
    }, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Headphones"
    assert data["target_amount"] == "150.00"
    assert data["saved_amount"] == "0.00"
    assert data["progress"] == 0.0


def test_create_goal_invalid_amount(client, auth_header):
    """Target amount <= 0 devuelve 422."""
    response = client.post("/api/goals", json={
        "name": "Bad goal",
        "target_amount": 0,
    }, headers=auth_header)
    assert response.status_code == 422


def test_create_goal_without_deadline(client, auth_header):
    """Deadline es opcional."""
    response = client.post("/api/goals", json={
        "name": "Open goal",
        "target_amount": 100,
    }, headers=auth_header)
    assert response.status_code == 201
    assert response.json()["deadline"] is None


def test_get_goals_empty(client, auth_header):
    """Sin metas devuelve lista vacia."""
    response = client.get("/api/goals", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


def test_contribute_positive(client, auth_header):
    """Contribuir suma al saved_amount y actualiza progress."""
    create = client.post("/api/goals", json={
        "name": "Bike", "target_amount": 200,
    }, headers=auth_header)
    goal_id = create.json()["goal_id"]

    response = client.post(
        f"/api/goals/{goal_id}/contribute",
        json={"amount": 50},
        headers=auth_header,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["saved_amount"] == "50.00"
    assert data["progress"] == 25.0


def test_contribute_negative_to_withdraw(client, auth_header):
    """Amount negativo retira (withdraw)."""
    create = client.post("/api/goals", json={
        "name": "Trip", "target_amount": 500,
    }, headers=auth_header)
    goal_id = create.json()["goal_id"]
    client.post(
        f"/api/goals/{goal_id}/contribute",
        json={"amount": 100},
        headers=auth_header,
    )
    response = client.post(
        f"/api/goals/{goal_id}/contribute",
        json={"amount": -30},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["saved_amount"] == "70.00"


def test_contribute_cannot_go_negative(client, auth_header):
    """Withdraw que dejaria saved_amount < 0 devuelve 400."""
    create = client.post("/api/goals", json={
        "name": "Tight", "target_amount": 100,
    }, headers=auth_header)
    goal_id = create.json()["goal_id"]
    response = client.post(
        f"/api/goals/{goal_id}/contribute",
        json={"amount": -10},
        headers=auth_header,
    )
    assert response.status_code == 400
    assert "negative" in response.json()["detail"].lower()


def test_contribute_to_missing_goal(client, auth_header):
    """Contribuir a goal_id inexistente devuelve 404."""
    response = client.post(
        "/api/goals/9999/contribute",
        json={"amount": 10},
        headers=auth_header,
    )
    assert response.status_code == 404


def test_delete_goal(client, auth_header):
    """Eliminar meta y verificar que ya no aparece en GET."""
    create = client.post("/api/goals", json={
        "name": "Delete me", "target_amount": 50,
    }, headers=auth_header)
    goal_id = create.json()["goal_id"]
    response = client.delete(f"/api/goals/{goal_id}", headers=auth_header)
    assert response.status_code == 204

    listed = client.get("/api/goals", headers=auth_header).json()
    assert all(g["goal_id"] != goal_id for g in listed)


def test_delete_missing_goal(client, auth_header):
    """Eliminar goal inexistente devuelve 404."""
    response = client.delete("/api/goals/9999", headers=auth_header)
    assert response.status_code == 404


def test_goal_unauthorized(client):
    """Sin token devuelve 403."""
    response = client.get("/api/goals")
    assert response.status_code == 403
