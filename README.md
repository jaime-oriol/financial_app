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

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) or `conda create -n fapp python=3.11` |
| Flutter | 3.29+ | [flutter.dev/get-started](https://docs.flutter.dev/get-started/install) |
| Google Chrome | any | For running the frontend in web mode |

> **📦 Database:** The project uses a shared remote PostgreSQL on [Neon](https://neon.tech). No local database installation needed — all team members connect to the same cloud instance.

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

Edit `backend/.env` with the shared database credentials (ask a team member):

```env
DATABASE_URL=postgresql://neondb_owner:PASSWORD@ep-xxx.region.neon.tech/neondb?sslmode=require
JWT_SECRET=fapp-dev-secret-2026-change-in-prod
```

### 3. Start the backend

```bash
cd backend
uvicorn app.main:app --reload
```

The server will:
- Create all database tables automatically on first run
- Seed 6 default categories (Food, Transport, Entertainment, Health, Education, Other)
- Serve the API at `http://localhost:8000`
- Show interactive API docs at `http://localhost:8000/docs`

### 4. Start the frontend

Open a **second terminal**:

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

The app will open in Chrome and connect to the backend at `http://localhost:8000/api`.

> **💡 Tip:** Both the backend and frontend must be running at the same time. Keep two terminals open.

> **📱 Mobile:** To run on a physical Android device or emulator, the app auto-detects the platform and adjusts the API URL (`localhost` for web, `10.0.2.2` for Android emulator).

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
