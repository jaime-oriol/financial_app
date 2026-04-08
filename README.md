<div align="center">

# 💰 FAPP — Financial App

**Financial literacy app for teenagers (13–18)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.29-02569B?logo=flutter)](https://flutter.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 About

FAPP is a mobile application designed to help teenagers understand and practice basic financial skills — budgeting, saving, and responsible spending — through interactive tools and gamified learning.

Built as part of an academic project by **3:2 Analytics**, the app bridges the gap in financial education for young users (ages 13–18) by combining real expense tracking with engaging lessons, quizzes, and simulations.

## ✨ Features

### 🏦 Core (Backend + Frontend)
- **User Registration & Login** — JWT authentication with email/password
- **Expense Tracking** — Log expenses by amount, description, date and category
- **Budget Management** — Set monthly spending limits per category with real-time progress
- **Dashboard** — Spending by category chart, budget progress bars, recent transactions
- **6 Preset Categories** — Food, Transport, Entertainment, Health, Education, Other

### 📚 Gamification (Frontend mock)
- **Financial Lessons** — Structured modules: Budgeting basics, Needs vs. Wants, Saving money, etc.
- **Daily Challenges** — Quick quizzes to earn XP
- **Achievement Badges** — First Saver, Hot Streak, Budget Pro
- **Savings Goals** — Visual goal tracking with behind-pace warnings

### 🎯 Aligned with Use Cases
| UC | Feature | Status |
|----|---------|--------|
| UC-01 | Register Account | ✅ Functional |
| UC-02 | Add Expense (manual) | ✅ Functional |
| UC-03 | Create Monthly Budget | ✅ Functional |
| UC-04 | View Expense History | ✅ Functional |
| UC-05 | View Dashboard / Analytics | ✅ Functional |

---

## 🏗️ Architecture

```
FAPP/
├── backend/                  # Python FastAPI REST API
│   ├── app/
│   │   ├── models/           # SQLAlchemy ORM (User, Category, Expense, Budget)
│   │   ├── schemas/          # Pydantic validation (request/response)
│   │   ├── routers/          # API endpoints (auth, expenses, budgets, dashboard)
│   │   ├── services/         # Business logic layer
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Environment settings
│   │   ├── database.py       # DB connection & session
│   │   └── seed.py           # Initial category data
│   ├── alembic/              # Database migrations
│   ├── tests/                # 23 pytest tests
│   └── requirements.txt
│
├── frontend/                 # Flutter mobile app
│   └── lib/
│       ├── model/            # Data models (User, Category, Expense, Budget, Dashboard)
│       ├── services/         # API client (HTTP + JWT)
│       ├── providers/        # Riverpod state management
│       ├── pages/            # UI screens (auth, dashboard, budget, lessons, goals, profile)
│       ├── ui/               # Theme, widgets, sizing constants
│       ├── constants/        # Colors, icons, shadows
│       ├── routes/           # Navigation configuration
│       └── main.dart
│
└── docs/                     # Project documentation (PDF)
    ├── OPPR.pdf              # Objectives, Project Plan and Requirements
    └── Solution_design.pdf   # Use cases, diagrams, wireframes, DB schema
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Flutter | 3.29+ | Frontend framework |
| Conda (optional) | any | Python environment management |

> **Database:** The project uses a shared remote PostgreSQL instance on [Neon](https://neon.tech) — no local database setup needed.

### 1. Clone the repository

```bash
git clone https://github.com/jaime-oriol/financial_app.git
cd financial_app
```

### 2. Backend setup

```bash
# Create and activate Python environment
conda create -n fapp python=3.11 -y
conda activate fapp

# Install dependencies
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `backend/.env` with the shared Neon database URL (ask a team member for the credentials):

```
DATABASE_URL=postgresql://neondb_owner:PASSWORD@ep-PROJECT.region.neon.tech/neondb?sslmode=require
JWT_SECRET=fapp-dev-secret-2026-change-in-prod
```

```bash
# Run the server (creates tables + seeds categories automatically on first run)
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 4. Run backend tests

```bash
cd backend
python -m pytest tests/ -v
```

All 23 tests run against SQLite in-memory (no PostgreSQL needed for testing).

### 5. Frontend setup

```bash
cd frontend

# Install Flutter dependencies
flutter pub get

# Run the app (connect a device or start an emulator first)
flutter run
```

> **Note:** The Flutter app connects to `http://10.0.2.2:8000/api` by default (Android emulator). For physical devices, update `_baseUrl` in `lib/services/api_client.dart` to your machine's local IP.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Create new account | No |
| POST | `/api/auth/login` | Login & get JWT | No |
| GET | `/api/categories` | List all categories | No |
| POST | `/api/expenses` | Create expense | Yes |
| GET | `/api/expenses` | List expenses (with filters) | Yes |
| POST | `/api/budgets` | Create monthly budget | Yes |
| GET | `/api/budgets` | List budgets for month/year | Yes |
| GET | `/api/dashboard` | Dashboard summary | Yes |
| GET | `/health` | Health check | No |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Async Python web framework
- **SQLAlchemy 2.0** — ORM with mapped columns
- **Alembic** — Database migrations
- **PostgreSQL** — Relational database
- **JWT (python-jose)** — Token-based authentication
- **Pydantic v2** — Request/response validation
- **pytest** — Testing framework

### Frontend
- **Flutter 3.29** — Cross-platform UI framework
- **Riverpod** — State management
- **fl_chart** — Donut/pie charts
- **http** — REST API client
- **shared_preferences** — Local JWT storage

---

## 📊 Database Schema

Four main tables aligned with the Entity Relationship Diagram:

| Table | Primary Key | Key Columns |
|-------|-------------|-------------|
| **users** | user_id (INT) | name, surname, birthdate, email (UNIQUE), password_hash |
| **categories** | category_id (INT) | name, icon, description |
| **expenses** | expense_id (INT) | user_id FK, category_id FK, amount, description, expense_date |
| **budgets** | budget_id (INT) | user_id FK, category_id FK, month, year, limit_amount |

---

## 📄 Documentation

Full project documentation is available in the `docs/` folder:
- **OPPR.pdf** — Objectives, requirements, milestones, use case diagrams, Gantt chart
- **Solution_design.pdf** — Use cases, activity/sequence/class diagrams, ERD, DB schema, wireframes

---

## 👥 Team

**3:2 Analytics** — Academic project, 2026

---

## 📝 License

This project is licensed under the MIT License.
