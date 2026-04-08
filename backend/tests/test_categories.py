"""Tests de categorias: verifica que las 6 seeds se cargan correctamente."""


def test_get_categories(client):
    """Las 6 categorias seed estan disponibles."""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    names = [c["name"] for c in data]
    assert names == ["Food", "Transport", "Entertainment", "Health", "Education", "Other"]
