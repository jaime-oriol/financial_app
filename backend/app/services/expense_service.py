"""Logica de negocio para gastos. Separa la BD del router."""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.schemas.expense import ExpenseResponse


def build_expense_response(expense: Expense, category: Category | None) -> ExpenseResponse:
    """Construir response con nombre de categoria incluido."""
    return ExpenseResponse(
        expense_id=expense.expense_id,
        user_id=expense.user_id,
        category_id=expense.category_id,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        created_at=expense.created_at,
        category_name=category.name if category else None,
    )


def find_expenses(
    db: Session,
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
) -> list[ExpenseResponse]:
    """Buscar gastos del usuario con filtros opcionales (fecha, categoria)."""
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    if category_id:
        query = query.filter(Expense.category_id == category_id)

    expenses = query.order_by(Expense.expense_date.desc()).all()

    # Cargar categorias en batch para evitar N+1 queries
    cat_ids = {e.category_id for e in expenses}
    categories = {
        c.category_id: c
        for c in db.query(Category).filter(Category.category_id.in_(cat_ids)).all()
    }

    return [build_expense_response(e, categories.get(e.category_id)) for e in expenses]


def get_total_spent(db: Session, user_id: int, category_id: int, month: int, year: int) -> Decimal:
    """Calcular total gastado por usuario en una categoria para un mes/anio."""
    from sqlalchemy import extract, func

    result = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.category_id == category_id,
            extract("month", Expense.expense_date) == month,
            extract("year", Expense.expense_date) == year,
        )
        .scalar()
    )
    return Decimal(str(result))
