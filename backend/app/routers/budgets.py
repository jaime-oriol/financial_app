"""Endpoints de presupuestos mensuales por categoria."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.budget import Budget
from app.models.category import Category
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.services.auth import get_current_user
from app.services.budget_service import build_budget_response, find_budgets
from app.services.expense_service import get_total_spent

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """UC-03: Create monthly budget (by category).
    Sequence: validateAmount -> getBudget(userId, category) -> check exists -> create -> 201.
    """
    # Validar que la categoria existe
    category = db.query(Category).filter(Category.category_id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    # Validar que no exista ya un presupuesto para esa categoria/mes/anio
    existing = (
        db.query(Budget)
        .filter(
            Budget.user_id == user.user_id,
            Budget.category_id == data.category_id,
            Budget.month == data.month,
            Budget.year == data.year,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this category and month",
        )

    budget = Budget(
        user_id=user.user_id,
        category_id=data.category_id,
        month=data.month,
        year=data.year,
        limit_amount=data.limit_amount,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)

    spent = get_total_spent(db, user.user_id, data.category_id, data.month, data.year)
    return build_budget_response(budget, category, spent)


@router.get("", response_model=list[BudgetResponse])
def get_budgets(
    month: int = Query(default=None),
    year: int = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Listar presupuestos del mes actual o del mes/anio indicado."""
    today = date.today()
    m = month or today.month
    y = year or today.year
    return find_budgets(db, user.user_id, m, y)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Eliminar un presupuesto del usuario (CRUD completo, transaccional)."""
    budget = (
        db.query(Budget)
        .filter(Budget.budget_id == budget_id, Budget.user_id == user.user_id)
        .first()
    )
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    db.delete(budget)
    db.commit()
