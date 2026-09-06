# Mini Order Quality System

A deliberately small order-management app for learning how a QA engineer builds a test system end-to-end.

## Business features

- Login
- Create order
- List orders
- Refund order

Business rules:

- `paid` orders can be refunded.
- `shipped` orders cannot be refunded.
- `refunded` orders cannot be refunded twice.

Demo login:

```text
username: qa
password: qa123
```

## Why this repository exists

This project is intentionally simple so the focus stays on quality engineering:

```text
Application
  ↓
Unit tests
  ↓
API tests
  ↓
UI / E2E smoke tests
  ↓
pytest markers
  ↓
GitHub Actions
  ↓
PR smoke gate
  ↓
Nightly regression
```

## Project structure

```text
mini-order-quality-system/
├── app/                     # FastAPI application
│   ├── main.py
│   ├── database.py
│   └── services/
├── templates/               # Minimal web UI
├── tests/
│   ├── unit/                # developer-style unit tests
│   ├── api/                 # API tests
│   └── ui/                  # Playwright E2E
├── .github/workflows/
│   ├── pr-smoke.yml         # PR / main smoke checks
│   └── nightly-regression.yml
├── pytest.ini
└── requirements.txt
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Run tests

```bash
pytest -q
pytest -m smoke -q
pytest tests/api -q
pytest tests/ui -q
```

## CI/CD learning path

- Pull Request: `.github/workflows/pr-smoke.yml` runs smoke checks.
- Nightly: `.github/workflows/nightly-regression.yml` runs the full pytest suite every night and supports manual execution.

## Next learning steps

1. Add Allure reports.
2. Save Playwright screenshots/trace on failure.
3. Add test data factories.
4. Add Docker.
5. Add a staging deployment job.
6. Make smoke tests a required GitHub branch check.
7. Add an Agent layer and Agent Eval dataset.
8. Add version-to-version quality metrics and release gates.
