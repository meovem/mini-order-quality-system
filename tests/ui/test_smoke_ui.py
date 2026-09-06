import os
import subprocess
import time

import pytest
import requests
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module")
def live_server():
    env = os.environ.copy()
    env["ORDER_DB_PATH"] = "ui_test_orders.db"
    process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], env=env)
    for _ in range(30):
        try:
            if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
                break
        except Exception:
            time.sleep(0.2)
    else:
        process.terminate()
        raise RuntimeError("server did not start")
    yield
    process.terminate()
    process.wait(timeout=5)
    try:
        os.remove("ui_test_orders.db")
    except FileNotFoundError:
        pass


@pytest.mark.smoke
def test_login_create_order_and_refund(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)
        page.fill('input[name="username"]', "qa")
        page.fill('input[name="password"]', "qa123")
        page.click("#login-button")
        page.wait_for_url("**/orders")
        page.fill('input[name="product_name"]', "Playwright Book")
        page.fill('input[name="amount"]', "88")
        page.click('button:has-text("Create Order")')
        row = page.locator("tbody tr").first
        assert "Playwright Book" in row.inner_text()
        assert "paid" in row.inner_text()
        row.locator('button:has-text("Refund")').click()
        page.wait_for_url("**/orders")
        assert "refunded" in page.locator("tbody tr").first.inner_text()
        browser.close()
