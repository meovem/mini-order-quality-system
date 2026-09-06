from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.database import init_db
from app.services.auth import authenticate
from app.services.order import create_order, get_order, list_orders, refund_order

app = FastAPI(title="Mini Order System", version="1.0.0")
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateOrderRequest(BaseModel):
    product_name: str = Field(min_length=1)
    amount: float = Field(gt=0)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/login")
def api_login(payload: LoginRequest):
    if not authenticate(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="invalid username or password")
    return {"success": True, "token": "demo-token"}


@app.get("/api/orders")
def api_orders():
    return {"items": list_orders()}


@app.get("/api/orders/{order_id}")
def api_order_detail(order_id: int):
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order


@app.post("/api/orders", status_code=201)
def api_create_order(payload: CreateOrderRequest):
    return create_order(payload.product_name, payload.amount)


@app.post("/api/orders/{order_id}/refund")
def api_refund(order_id: int):
    try:
        return refund_order(order_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login", response_class=HTMLResponse)
def login_web(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate(username, password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
            status_code=401,
        )
    return RedirectResponse(url="/orders", status_code=303)


@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": list_orders(), "error": None}
    )


@app.post("/orders")
def create_order_web(product_name: str = Form(...), amount: float = Form(...)):
    create_order(product_name, amount)
    return RedirectResponse(url="/orders", status_code=303)


@app.post("/orders/{order_id}/refund")
def refund_order_web(order_id: int):
    try:
        refund_order(order_id)
    except (LookupError, ValueError):
        pass
    return RedirectResponse(url="/orders", status_code=303)
