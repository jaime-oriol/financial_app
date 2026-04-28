"""Tests Challenges: list + submit (transaccional, XP server-side)."""


def test_list_challenges_seeded(client, auth_header):
    """Los challenges seed estan disponibles con su contenido en BD."""
    response = client.get("/api/challenges", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    kinds = {c["kind"] for c in data}
    assert {"quiz", "simulation"} <= kinds
    quiz = next(c for c in data if c["kind"] == "quiz")
    assert "questions" in quiz["content"]
    assert len(quiz["content"]["questions"]) >= 3
    sim = next(c for c in data if c["kind"] == "simulation")
    assert "choices" in sim["content"]


def test_list_challenges_status_initial(client, auth_header):
    """Sin intentos: completed=False y best_xp=0 para todos."""
    response = client.get("/api/challenges", headers=auth_header)
    for c in response.json():
        assert c["completed"] is False
        assert c["best_xp"] == 0


def test_quiz_attempt_xp_calculated_server_side(client, auth_header):
    """Score 2/3 -> xp_earned = 20 (server calcula score*10, cliente no decide)."""
    response = client.post(
        "/api/challenges/1/attempt",
        json={"payload": {"score": 2, "total": 3}},
        headers=auth_header,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["xp_earned"] == 20
    assert data["payload"] == {"score": 2, "total": 3}


def test_quiz_perfect_score(client, auth_header):
    """Score 3/3 -> xp_earned = 30 (max)."""
    response = client.post(
        "/api/challenges/1/attempt",
        json={"payload": {"score": 3, "total": 3}},
        headers=auth_header,
    )
    assert response.json()["xp_earned"] == 30


def test_simulation_xp_from_choice(client, auth_header):
    """Choice 1 (Smart) -> xp_earned = 25 desde content.choices[1].xp."""
    response = client.post(
        "/api/challenges/2/attempt",
        json={"payload": {"choice_idx": 1}},
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.json()["xp_earned"] == 25


def test_simulation_xp_per_choice(client, auth_header):
    """Cada eleccion da el XP definido en BD para esa choice."""
    expected = {0: 5, 1: 25, 2: 15}
    for idx, expected_xp in expected.items():
        response = client.post(
            "/api/challenges/2/attempt",
            json={"payload": {"choice_idx": idx}},
            headers=auth_header,
        )
        assert response.json()["xp_earned"] == expected_xp


def test_attempt_to_missing_challenge(client, auth_header):
    """Challenge inexistente devuelve 404."""
    response = client.post(
        "/api/challenges/9999/attempt",
        json={"payload": {"score": 1, "total": 3}},
        headers=auth_header,
    )
    assert response.status_code == 404


def test_challenges_status_after_attempt(client, auth_header):
    """Tras un intento: completed=True, best_xp = xp del intento."""
    client.post(
        "/api/challenges/1/attempt",
        json={"payload": {"score": 2, "total": 3}},
        headers=auth_header,
    )
    response = client.get("/api/challenges", headers=auth_header)
    quiz = next(c for c in response.json() if c["challenge_id"] == 1)
    assert quiz["completed"] is True
    assert quiz["best_xp"] == 20


def test_challenges_best_xp_keeps_max(client, auth_header):
    """Tras varios intentos, best_xp = max de todos."""
    for score in [1, 3, 2]:  # 10, 30, 20
        client.post(
            "/api/challenges/1/attempt",
            json={"payload": {"score": score, "total": 3}},
            headers=auth_header,
        )
    response = client.get("/api/challenges", headers=auth_header)
    quiz = next(c for c in response.json() if c["challenge_id"] == 1)
    assert quiz["best_xp"] == 30


def test_challenges_unauthorized(client):
    """Sin token devuelve 403."""
    response = client.get("/api/challenges")
    assert response.status_code == 403
