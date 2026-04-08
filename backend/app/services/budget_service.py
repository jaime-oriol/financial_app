"""Logica de negocio para presupuestos mensuales."""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.schemas.budget import BudgetResponse
from app.services.expense_service import get_total_spent


def build_budget_response(budget: Budget, category: Category | None, spent: Decimal) -> BudgetResponse:
    """Construir response con progreso de gasto calculado."""
    progress = float(spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0.0
    return BudgetResponse(
        budget_id=budget.budget_id,
        user_id=budget.user_id,
        category_id=budget.category_id,
        month=budget.month,
        year=budget.year,
        limit_amount=budget.limit_amount,
        created_at=budget.created_at,
        category_name=category.name if category else None,
        spent=spent,
        progress=round(progress, 1),
    )


def find_budgets(db: Session, user_id: int, month: int, year: int) -> list[BudgetResponse]:
    """Obtener todos los presupuestos del usuario para un mes/anio con progreso."""
    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year)
        .all()
    )

    # Cargar categorias en batch
    cat_ids = {b.category_id for b in budgets}
    categories = {
        c.category_id: c
        for c in db.query(Category).filter(Category.category_id.in_(cat_ids)).all()
    }

    result = []
    for b in budgets:
        spent = get_total_spent(db, user_id, b.category_id, month, year)
        result.append(build_budget_response(b, categories.get(b.category_id), spent))
    return result
