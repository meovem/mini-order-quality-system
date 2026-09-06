import pytest


@pytest.mark.smoke
def test_login_success(client):
    response = client.post("/api/login", json={"username": "qa", "password": "qa123"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_login_failure(client):
    response = client.post("/api/login", json={"username": "qa", "password": "bad"})
    assert response.status_code == 401
