"""Schemas del dashboard: gasto por categoria, streak y resumen financiero."""

from decimal import Decimal

from pydantic import BaseModel

from app.schemas.budget import BudgetResponse
from app.schemas.expense import ExpenseResponse


class SpendingByCategory(BaseModel):
    category_id: int
    category_name: str
    total: Decimal


class DashboardResponse(BaseModel):
    spending_by_category: list[SpendingByCategory]
    budgets: list[BudgetResponse]
    recent_transactions: list[ExpenseResponse]
    streak: int = 0  # Dias consecutivos con al menos un gasto registrado
    total_expenses: int = 0  # Numero total de gastos del usuario
