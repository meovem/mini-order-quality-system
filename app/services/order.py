from app.database import get_conn


def list_orders():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, product_name, amount, status FROM orders ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def create_order(product_name: str, amount: float):
    if not product_name.strip():
        raise ValueError("product_name is required")
    if amount <= 0:
        raise ValueError("amount must be greater than 0")
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO orders(product_name, amount, status) VALUES (?, ?, 'paid')",
            (product_name.strip(), amount),
        )
        order_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, product_name, amount, status FROM orders WHERE id = ?",
            (order_id,),
        ).fetchone()
        return dict(row)


def get_order(order_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, product_name, amount, status FROM orders WHERE id = ?",
            (order_id,),
        ).fetchone()
        return dict(row) if row else None


def refund_order(order_id: int):
    order = get_order(order_id)
    if not order:
        raise LookupError("order not found")
    if order["status"] == "shipped":
        raise ValueError("shipped order cannot be refunded")
    if order["status"] == "refunded":
        raise ValueError("order already refunded")
    with get_conn() as conn:
        conn.execute("UPDATE orders SET status = 'refunded' WHERE id = ?", (order_id,))
    return get_order(order_id)
