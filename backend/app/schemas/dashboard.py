"""Schemas del dashboard: gasto por categoria, streak, daily trend, resumen."""

from datetime import date as date_type
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.budget import BudgetResponse
from app.schemas.expense import ExpenseResponse


class SpendingByCategory(BaseModel):
    category_id: int
    category_name: str
    total: Decimal


class DailyTotal(BaseModel):
    date: date_type
    total: Decimal


class Achievement(BaseModel):
    id: str
    name: str
    icon: str
    color: str
    description: str
    earned: bool


class DashboardResponse(BaseModel):
    spending_by_category: list[SpendingByCategory]
    budgets: list[BudgetResponse]
    recent_transactions: list[ExpenseResponse]
    streak: int = 0  # Dias consecutivos con al menos un gasto registrado
    total_expenses: int = 0  # Numero total de gastos del usuario
    daily_spending: list[DailyTotal] = []  # Ultimos 7 dias para trend chart
    total_xp: int = 0  # XP acumulado por challenges completados
    challenges_done: int = 0  # Numero de challenges intentados
    achievements: list[Achievement] = []  # Badges calculados desde BD
