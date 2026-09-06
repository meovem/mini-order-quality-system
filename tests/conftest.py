import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DB = Path("test_orders.db")
os.environ["ORDER_DB_PATH"] = str(TEST_DB)

from app.database import init_db
from app.main import app


@pytest.fixture(autouse=True)
def reset_db():
    if TEST_DB.exists():
        TEST_DB.unlink()
    init_db()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture
def client():
    return TestClient(app)
