<div align="center">

<img src="./docs/logo.png" width="120" alt="FAPP logo">

# FAPP — Financial App

**Financial literacy app for teenagers (13–18)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-2.13-3b9eff)](https://nicegui.io/)
[![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00e599?logo=postgresql)](https://neon.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## About

FAPP is a web app designed to help teenagers understand and practice basic financial skills — budgeting, saving, and responsible spending — through real, transactional tracking and savings goals.

Academic project by **3:2 Analytics** (2026). Backend in FastAPI on Render, frontend in pure Python (NiceGUI) — no JS/CSS to write, deploys as a single process.

## Features

All transactional. No mocked or hardcoded data.

- **Auth** — JWT register/login with email + password
- **Dashboard** — total spending this month, real streak (consecutive days with expenses), 7-day spending trend chart, recent transactions
- **Budget tracker** — donut chart with center total, per-category progress bars, add/delete expenses, create/delete budgets
- **Challenges** — quiz + simulation challenges. Content stored in DB, attempts persisted, XP earned per attempt
- **Savings goals** — create goals with target + deadline, add/withdraw money via dialog, behind-pace warning derived from real progress vs time elapsed
- **Profile** — real stats (streak, XP, expense count, goal count, member since), logout

### Use cases covered

| UC | Feature | Status |
|----|---------|--------|
| UC-01 | Register Account | ✅ |
| UC-02 | Add Expense (manual) | ✅ |
| UC-03 | Create Monthly Budget | ✅ |
| UC-04 | View Expense History | ✅ |
| UC-05 | View Dashboard / Analytics | ✅ |
| Extra | Savings Goals (transactional +/-) | ✅ |
| Extra | Challenges (quiz + simulation, attempts persisted, XP) | ✅ |
| Extra | Real streak from expense history | ✅ |
| Extra | Full CRUD (delete expenses, budgets, goals) | ✅ |

---

## Architecture

```
financial_app/
├── backend/                  # FastAPI REST API
│   └── app/
│       ├── models/           # User, Category, Expense, Budget, Goal
│       ├── schemas/          # Pydantic request/response
│       ├── routers/          # auth, expenses, budgets, dashboard, goals
│       ├── services/         # auth, expense, budget, goal, dashboard
│       ├── main.py           # FastAPI app + CORS + lifespan seed
│       ├── config.py
│       ├── database.py
│       └── seed.py           # 6 preset categories
│
├── frontend/                 # NiceGUI Python web app
│   ├── app.py                # Entry point + page registration
│   ├── api.py                # HTTP client (httpx + JWT)
│   ├── state.py              # Session storage (cookies)
│   ├── theme.py              # Colors, icons, money formatting
│   ├── layout.py             # App shell, bottom nav, helpers
│   ├── dialogs.py            # Reusable transactional dialogs
│   └── pages/
│       ├── auth.py           # /login, /register
│       ├── home.py           # / (dashboard with trend chart)
│       ├── budget.py         # /budget (donut + bars + CRUD)
│       ├── challenges.py     # /challenges (hub: quiz + simulation cards)
│       ├── quiz.py           # /quiz/{id} (transactional)
│       ├── simulation.py     # /simulation/{id} (transactional)
│       ├── goals.py          # /goals (transactional +/-)
│       └── profile.py        # /profile (real stats, logout)
│
├── frontend_v2/              # OLD Flutter frontend (kept for reference)
└── docs/                     # OPPR.pdf, Solution_design.pdf, logo.png
```

---

## Getting Started

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |

> **Database:** Shared remote PostgreSQL on [Neon](https://neon.tech).
> **Backend deploy:** Render at [`https://fapp-api.onrender.com`](https://fapp-api.onrender.com/docs). Auto-redeploys on every push to `main`.

### 1. Clone the repository

```bash
git clone https://github.com/jaime-oriol/financial_app.git
cd financial_app
```

### 2. Frontend (recommended)

```bash
cd frontend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Opens at `http://localhost:8080`. Connects to the deployed backend by default.

To point at a local backend: `API_URL=http://localhost:8000/api .venv/bin/python app.py`

### 3. Backend (only if running locally)

```bash
cd backend
conda create -n fapp python=3.11 -y
conda activate fapp
pip install -r requirements.txt
cp .env.example .env  # edit with shared Neon credentials
uvicorn app.main:app --reload
```

API at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### 4. Run backend tests

```bash
cd backend
python -m pytest tests/ -v
```

23 tests against SQLite in-memory — no database connection required.

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Create account | ❌ |
| `POST` | `/api/auth/login` | Login → JWT | ❌ |
| `GET`  | `/api/auth/me` | Current user info | ✅ |
| `GET`  | `/api/categories` | List categories | ❌ |
| `POST` | `/api/expenses` | Create expense | ✅ |
| `GET`  | `/api/expenses` | List (filters: `start_date`, `end_date`, `category_id`) | ✅ |
| `DELETE` | `/api/expenses/{id}` | Delete expense | ✅ |
| `POST` | `/api/budgets` | Create monthly budget | ✅ |
| `GET`  | `/api/budgets` | List (filters: `month`, `year`) | ✅ |
| `DELETE` | `/api/budgets/{id}` | Delete budget | ✅ |
| `GET`  | `/api/dashboard` | Spending, streak, trend, budgets, recent | ✅ |
| `GET`  | `/api/goals` | List user goals | ✅ |
| `POST` | `/api/goals` | Create goal | ✅ |
| `POST` | `/api/goals/{id}/contribute` | Add or withdraw amount | ✅ |
| `DELETE` | `/api/goals/{id}` | Delete goal | ✅ |
| `GET`  | `/api/challenges` | List challenges with user status | ✅ |
| `POST` | `/api/challenges/{id}/attempt` | Submit attempt (XP server-side) | ✅ |
| `GET`  | `/health` | Health check | ❌ |

---

## Tech Stack

### Backend

- **FastAPI** — async Python web framework
- **SQLAlchemy 2.0** — ORM with `Mapped` columns
- **Alembic** — migrations
- **Neon (PostgreSQL)** — serverless cloud database
- **JWT (python-jose)** — auth
- **Pydantic v2** — request/response validation
- **pytest** — 23 tests (SQLite in-memory)

### Frontend

- **NiceGUI 2.13** — Python web UI (Quasar/Vue under the hood)
- **httpx** — async HTTP client
- **echart** — donut + area charts (via NiceGUI's `ui.echart`)
- Single-process Python — deploys anywhere FastAPI deploys

---

## Database Schema

Five tables on Neon (see `docs/Solution_design.pdf`, p.11 for ERD):

| Table | Primary Key | Key Columns |
|-------|-------------|-------------|
| **users** | user_id (INT) | name, surname, birthdate, email (UNIQUE), password (bcrypt) |
| **categories** | category_id (INT) | name, icon, description (6 seed rows) |
| **expenses** | expense_id (INT) | user_id FK, category_id FK, amount, description, expense_date |
| **budgets** | budget_id (INT) | user_id FK, category_id FK, month, year, limit_amount |
| **goals** | goal_id (INT) | user_id FK, name, target_amount, saved_amount, deadline |

---

## Documentation

- **OPPR.pdf** — Objectives, requirements, milestones, use case diagrams
- **Solution_design.pdf** — Use cases, sequence/class diagrams, ERD, wireframes

---

## Team

**3:2 Analytics** — Academic project, 2026

## License

MIT
