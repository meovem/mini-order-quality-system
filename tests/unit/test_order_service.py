import pytest
from app.services.order import create_order, refund_order


def test_create_order_defaults_to_paid():
    order = create_order("Keyboard", 199.0)
    assert order["status"] == "paid"


def test_paid_order_can_be_refunded():
    order = create_order("Mouse", 99.0)
    refunded = refund_order(order["id"])
    assert refunded["status"] == "refunded"


def test_refunded_order_cannot_be_refunded_again():
    order = create_order("Monitor", 999.0)
    refund_order(order["id"])
    with pytest.raises(ValueError, match="already refunded"):
        refund_order(order["id"])
