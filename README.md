<div align="center">

<img src="./docs/logo.png" width="120" alt="FAPP logo">

# 💰 FAPP — Financial App

**Financial literacy app for teenagers (13–18)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.29-02569B?logo=flutter)](https://flutter.dev/)
[![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00e599?logo=postgresql)](https://neon.tech/)
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

### 📚 Gamification
- **Financial Lessons** — Structured modules: Budgeting basics, Needs vs. Wants, Saving money, etc.
- **Quiz** — Multiple-choice questions with instant feedback, explanations, and XP rewards
- **Financial Simulation** — Real-life scenario ($200 budget split) with outcome cards
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
├── frontend/                 # Flutter cross-platform app
│   ├── assets/               # Logo and images
│   └── lib/
│       ├── model/            # Data models (User, Category, Expense, Budget, Dashboard)
│       ├── services/         # API client (HTTP + JWT)
│       ├── providers/        # Riverpod state management
│       ├── pages/            # UI screens
│       │   ├── auth/         # Register & Login
│       │   ├── dashboard/    # Home with spending summary
│       │   ├── budget/       # Budget tracker with donut chart
│       │   ├── lessons/      # Financial education modules
│       │   ├── quiz/         # Multiple-choice quiz with XP
│       │   ├── simulation/   # Financial decision scenario
│       │   ├── goals/        # Savings goal tracker
│       │   └── profile/      # User profile & settings
│       ├── ui/               # Theme, widgets, sizing constants
│       ├── constants/        # Colors, icons, shadows
│       ├── routes/           # Navigation configuration
│       └── main.dart
│
└── docs/                     # Project documentation (PDF)
    ├── OPPR.pdf              # Objectives, Project Plan and Requirements
    ├── Solution_design.pdf   # Use cases, diagrams, wireframes, DB schema
    └── logo.png              # Project logo
```

---

## 🚀 Getting Started

### Prerequisites

**To run the app in Chrome (web):**

| Tool | Version |
|------|---------|
| Flutter | 3.29+ |
| Google Chrome | (download [here](https://www.google.com/chrome/)) |

**To use on Android phone:** Just download the APK from [GitHub Releases](https://github.com/jaime-oriol/financial_app/releases) — nothing else needed.

**To run the backend locally (optional):**

| Tool | Version |
|------|---------|
| Python | 3.11+ |

> **📦 Database:** Shared remote PostgreSQL on [Neon](https://neon.tech).
>
> **🌐 Backend:** Deployed on [Render](https://render.com) at [`https://fapp-api.onrender.com`](https://fapp-api.onrender.com/docs). Auto-redeploys on every push to `main`.

### 1. Clone the repository

```bash
git clone https://github.com/jaime-oriol/financial_app.git
cd financial_app
```

### 2. Frontend (Web in Chrome)

**Recommended for team testing — no mobile device needed.**

First, install Flutter if not already installed:
```bash
git clone https://github.com/flutter/flutter.git -b stable ~/flutter
export PATH="$PATH:$HOME/flutter/bin"
flutter --version
```

Then run the app:
```bash
cd frontend
flutter pub get
flutter run -d chrome
```

This opens the app in Google Chrome at `http://localhost:9099`.

**Press `r` to hot-reload after code changes, `q` to quit.**

### 3. Frontend (Android APK)

**Easiest option:** Download the pre-built APK from [GitHub Releases](https://github.com/jaime-oriol/financial_app/releases):

1. Go to [Releases](https://github.com/jaime-oriol/financial_app/releases)
2. Download the latest `app-release.apk`
3. Transfer to your Android phone and install

> **📱 The APK connects directly to the deployed backend** — no local setup needed.
> **🔄 Auto-builds:** Every push to `main` automatically compiles a new APK to Releases.

### 4. Backend (local development, optional)

Only needed if you want to run the backend locally. The production backend is already deployed at [fapp-api.onrender.com](https://fapp-api.onrender.com/docs).

```bash
conda create -n fapp python=3.11 -y
conda activate fapp
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env` with shared database credentials (ask a team member):

```env
DATABASE_URL=postgresql://neondb_owner:PASSWORD@ep-xxx.region.neon.tech/neondb?sslmode=require
JWT_SECRET=fapp-dev-secret-2026-change-in-prod
```

```bash
uvicorn app.main:app --reload
```

API at `http://localhost:8000` | Docs at `http://localhost:8000/docs`

### 5. Run backend tests

```bash
cd backend
conda activate fapp
python -m pytest tests/ -v
```

All 23 tests run against SQLite in-memory — no database connection needed for testing.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Create new account | ❌ |
| `POST` | `/api/auth/login` | Login & get JWT token | ❌ |
| `GET` | `/api/categories` | List all categories | ❌ |
| `POST` | `/api/expenses` | Create expense | ✅ |
| `GET` | `/api/expenses` | List expenses (filters: `start_date`, `end_date`, `category_id`) | ✅ |
| `POST` | `/api/budgets` | Create monthly budget | ✅ |
| `GET` | `/api/budgets` | List budgets (filters: `month`, `year`) | ✅ |
| `GET` | `/api/dashboard` | Dashboard summary (spending, budgets, transactions) | ✅ |
| `GET` | `/health` | Health check | ❌ |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Async Python web framework
- **SQLAlchemy 2.0** — ORM with mapped columns
- **Alembic** — Database migrations
- **Neon (PostgreSQL)** — Serverless cloud database
- **JWT (python-jose)** — Token-based authentication
- **Pydantic v2** — Request/response validation
- **pytest** — Testing framework (23 tests)

### Frontend
- **Flutter 3.29** — Cross-platform UI framework (web, Android, iOS)
- **Riverpod** — State management
- **fl_chart** — Donut/pie charts for spending visualization
- **http** — REST API client
- **shared_preferences** — Local JWT token storage

---

## 📊 Database Schema

Four main tables hosted on Neon, aligned with the Entity Relationship Diagram (see `docs/Solution_design.pdf`, p.11):

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
