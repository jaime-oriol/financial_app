"""Logica del dashboard: agrega datos de gastos, presupuestos y transacciones recientes."""

from datetime import date
from decimal import Decimal

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.schemas.dashboard import DashboardResponse, SpendingByCategory
from app.services.budget_service import find_budgets
from app.services.expense_service import find_expenses


def get_dashboard(db: Session, user_id: int) -> DashboardResponse:
    """UC-05: View dashboard / simple analytics.
    Sequence: getSpendingByCategory -> getBudgetProgress -> getRecentTransactions -> 200.
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

    return DashboardResponse(
        spending_by_category=spending_by_category,
        budgets=budgets,
        recent_transactions=recent,
    )
