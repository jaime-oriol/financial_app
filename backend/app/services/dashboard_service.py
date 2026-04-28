"""Logica del dashboard: agrega datos de gastos, presupuestos, transacciones
recientes y calcula streak real (dias consecutivos con gasto registrado).
"""

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import distinct, extract, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.schemas.dashboard import DashboardResponse, SpendingByCategory
from app.services.budget_service import find_budgets
from app.services.expense_service import find_expenses


def compute_streak(db: Session, user_id: int) -> int:
    """Dias consecutivos (terminando hoy) con al menos un gasto registrado.
    Cumple feedback del profesor: streak debe ser real, no hardcoded.
    """
    rows = (
        db.query(distinct(Expense.expense_date))
        .filter(Expense.user_id == user_id)
        .all()
    )
    expense_dates = {row[0] for row in rows}
    streak = 0
    cursor = date.today()
    while cursor in expense_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def get_dashboard(db: Session, user_id: int) -> DashboardResponse:
    """UC-05: View dashboard / simple analytics.
    Sequence: getSpendingByCategory -> getBudgetProgress -> getRecentTransactions
              -> computeStreak -> 200.
    """
    today = date.today()

    # 1. Gasto por categoria del mes actual
    spending_rows = (
        db.query(
            Expense.category_id,
            Category.name,
            func.sum(Expense.amount).label("total"),
        )
        .join(Category, Expense.category_id == Category.category_id)
        .filter(
            Expense.user_id == user_id,
            extract("month", Expense.expense_date) == today.month,
            extract("year", Expense.expense_date) == today.year,
        )
        .group_by(Expense.category_id, Category.name)
        .all()
    )
    spending_by_category = [
        SpendingByCategory(
            category_id=row.category_id,
            category_name=row.name,
            total=Decimal(str(row.total)),
        )
        for row in spending_rows
    ]

    # 2. Progreso de presupuestos del mes actual
    budgets = find_budgets(db, user_id, today.month, today.year)

    # 3. Ultimas 5 transacciones
    recent = find_expenses(db, user_id)[:5]

    # 4. Streak real
    streak = compute_streak(db, user_id)

    # 5. Total de gastos historico (para profile stats)
    total_expenses = (
        db.query(func.count(Expense.expense_id))
        .filter(Expense.user_id == user_id)
        .scalar()
    ) or 0

    return DashboardResponse(
        spending_by_category=spending_by_category,
        budgets=budgets,
        recent_transactions=recent,
        streak=streak,
        total_expenses=total_expenses,
    )
