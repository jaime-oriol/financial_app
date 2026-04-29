<div align="center">

<img src="./docs/logo.png" width="120" alt="FAPP logo">

# FAPP — Financial App

**Financial literacy app for teenagers (13–18)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-2.13-3b9eff)](https://nicegui.io/)
[![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00e599?logo=postgresql)](https://neon.tech/)
[![Tests](https://img.shields.io/badge/tests-64_passing-success)](backend/tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Live Demo

| Service | URL |
|---------|-----|
| **Frontend** | https://fapp-web.onrender.com |
| **Backend API** | https://fapp-api.onrender.com |
| **API Docs** | https://fapp-api.onrender.com/docs |

Both services auto-redeploy on every push to `main`.

---

## About

FAPP helps teenagers practice budgeting, saving and responsible spending through real, transactional tracking. Academic project by **3:2 Analytics** (2026). Backend in FastAPI on Render, frontend in pure Python (NiceGUI).

Every interaction is transactional: streaks are computed from expense history, savings goals are persisted with every contribution, XP is calculated server-side from challenge attempts, and achievements are derived from the user's actual data.

## Features

- **Authentication** — JWT register / login with bcrypt-hashed passwords
- **Dashboard** — total spending this month, real streak (consecutive days with expenses), 7-day spending trend chart, budget usage, recent transactions
- **Budget tracker** — donut chart with center total, per-category progress bars, full CRUD on expenses and budgets
- **Savings goals** — create goals with target and deadline, add or withdraw money via dialog, behind-pace warning derived from real progress over time
- **Challenges** — quiz and simulation challenges with content stored in DB; attempts persisted, XP calculated server-side; progressive level unlock (Beginner → Intermediate → Advanced)
- **Achievements** — five badges computed live from the user's data (Hot Streak, First Saver, Budget Pro, Quiz Master, Goal Crusher)
- **Profile** — real stats: streak, total XP, expenses count, goals count, member since; photo avatar upload

### Use cases covered

| UC | Feature |
|----|---------|
| UC-01 | Register Account |
| UC-02 | Add Expense |
| UC-03 | Create Monthly Budget |
| UC-04 | View Expense History |
| UC-05 | View Dashboard / Analytics |

---

## Architecture

```
financial_app/
├── backend/                  # FastAPI REST API
│   └── app/
│       ├── models/           # User, Category, Expense, Budget, Goal, Challenge, ChallengeAttempt
│       ├── schemas/          # Pydantic request / response
│       ├── routers/          # auth, expenses, budgets, dashboard, goals, challenges, categories
│       ├── services/         # auth, expense, budget, goal, challenge, dashboard, achievements
│       ├── main.py           # FastAPI app + CORS + lifespan seed
│       ├── config.py
│       ├── database.py
│       └── seed.py           # 6 categories + challenges (quiz + simulation, multi-level)
│
├── frontend/                 # NiceGUI Python web app
│   ├── app.py                # Entry point + page registration
│   ├── api.py                # HTTP client (httpx + JWT)
│   ├── state.py              # Session storage (cookies)
│   ├── theme.py              # Colors, icons, money formatting
│   ├── layout.py             # App shell + bottom nav + helpers
│   ├── dialogs.py            # Reusable transactional dialogs
│   └── pages/
│       ├── auth.py           # /login, /register
│       ├── home.py           # / (dashboard with trend chart)
│       ├── budget.py         # /budget (donut + bars + CRUD)
│       ├── challenges.py     # /challenges (hub: quiz + simulation cards)
│       ├── quiz.py           # /quiz/{id}
│       ├── simulation.py     # /simulation/{id}
│       ├── goals.py          # /goals
│       └── profile.py        # /profile
│
└── docs/                     # OPPR.pdf, Solution_design.pdf, logo.png
```

---

## Getting Started

### Prerequisites

- Python 3.11+

> **Database:** Shared PostgreSQL on [Neon](https://neon.tech).  
> **Backend:** Deployed on Render at [`https://fapp-api.onrender.com`](https://fapp-api.onrender.com/docs). Auto-redeploys on every push to `main`.  
> **Frontend:** Deployed on Render at [`https://fapp-web.onrender.com`](https://fapp-web.onrender.com). Auto-redeploys on every push to `main`.

### 1. Clone the repository

```bash
git clone https://github.com/jaime-oriol/financial_app.git
cd financial_app
```

### 2. Run frontend locally

```bash
cd frontend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Opens at `http://localhost:8080`. Connects to the deployed backend by default.

To point at a local backend: `API_URL=http://localhost:8000/api .venv/bin/python app.py`

### 3. Run backend locally (only needed for local development)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env  # edit with shared Neon credentials
.venv/bin/uvicorn app.main:app --reload
```

API at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### 4. Run backend tests

```bash
cd backend
.venv/bin/python -m pytest tests/ -v
```

64 tests against SQLite in-memory — no Neon connection needed.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Create account |
| `POST` | `/api/auth/login` | Login and obtain JWT |
| `GET`  | `/api/auth/me` | Current user info |
| `PATCH` | `/api/auth/me` | Update avatar |
| `GET`  | `/api/categories` | List categories |
| `POST` | `/api/expenses` | Create expense |
| `GET`  | `/api/expenses` | List expenses (filters: `start_date`, `end_date`, `category_id`) |
| `DELETE` | `/api/expenses/{id}` | Delete expense |
| `POST` | `/api/budgets` | Create monthly budget |
| `GET`  | `/api/budgets` | List budgets (filters: `month`, `year`) |
| `DELETE` | `/api/budgets/{id}` | Delete budget |
| `GET`  | `/api/goals` | List user goals |
| `POST` | `/api/goals` | Create goal |
| `POST` | `/api/goals/{id}/contribute` | Add or withdraw amount |
| `DELETE` | `/api/goals/{id}` | Delete goal |
| `GET`  | `/api/challenges` | List challenges with user status |
| `POST` | `/api/challenges/{id}/attempt` | Submit attempt (XP computed server-side) |
| `GET`  | `/api/dashboard` | Spending breakdown, streak, trend, budgets, recent transactions, XP, achievements |
| `GET`  | `/health` | Health check |

---

## Tech Stack

### Backend

- **FastAPI** — async Python web framework
- **SQLAlchemy 2.0** — ORM with `Mapped` columns
- **Alembic** — database migrations
- **Neon (PostgreSQL)** — serverless cloud database
- **JWT (python-jose)** — token-based authentication
- **Pydantic v2** — request and response validation
- **pytest** — 64 tests covering every endpoint and business rule

### Frontend

- **NiceGUI 2.13** — Python web UI (Quasar / Vue under the hood)
- **httpx** — async HTTP client
- **echart** — donut and area charts via NiceGUI's `ui.echart`

---

## Database Schema

Seven tables on Neon (see `docs/Solution_design.pdf`, p. 11 for the ERD):

| Table | Primary Key | Key Columns |
|-------|-------------|-------------|
| **users** | user_id (INT) | name, surname, birthdate, email (UNIQUE), password (bcrypt), avatar (TEXT) |
| **categories** | category_id (INT) | name, icon, description |
| **expenses** | expense_id (INT) | user_id FK, category_id FK, amount, description, expense_date |
| **budgets** | budget_id (INT) | user_id FK, category_id FK, month, year, limit_amount |
| **goals** | goal_id (INT) | user_id FK, name, target_amount, saved_amount, deadline |
| **challenges** | challenge_id (INT) | kind, title, content (JSON), xp_reward, level |
| **challenge_attempts** | attempt_id (INT) | user_id FK, challenge_id FK, payload (JSON), xp_earned |

---

## Documentation

- **OPPR.pdf** — Objectives, requirements, milestones, use case diagrams
- **Solution_design.pdf** — Use cases, sequence and class diagrams, ERD, wireframes

---

## Team

**3:2 Analytics** — Academic project, 2026

## License

MIT
