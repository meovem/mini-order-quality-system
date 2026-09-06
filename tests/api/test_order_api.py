import pytest


@pytest.mark.smoke
def test_create_and_refund_order(client):
    create_resp = client.post("/api/orders", json={"product_name": "QA Book", "amount": 49.9})
    assert create_resp.status_code == 201
    order = create_resp.json()
    assert order["status"] == "paid"
    refund_resp = client.post(f"/api/orders/{order['id']}/refund")
    assert refund_resp.status_code == 200
    assert refund_resp.json()["status"] == "refunded"


def test_nonexistent_order_returns_404(client):
    assert client.get("/api/orders/999999").status_code == 404


def test_invalid_amount_is_rejected(client):
    response = client.post("/api/orders", json={"product_name": "Bad Order", "amount": 0})
    assert response.status_code == 422
