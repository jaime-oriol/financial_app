"""Endpoints de gastos: crear y listar con filtros."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.auth import get_current_user
from app.services.expense_service import build_expense_response, find_expenses

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """UC-02: Add expense (manual).
    Sequence: validateAmount -> findCategoryById -> insertExpense -> 201.
    """
    category = db.query(Category).filter(Category.category_id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    expense = Expense(
        user_id=user.user_id,
        category_id=data.category_id,
        amount=data.amount,
        description=data.description,
        expense_date=data.expense_date,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return build_expense_response(expense, category)


@router.get("", response_model=list[ExpenseResponse])
def get_expenses(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    category_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """UC-04: View expense history with optional filters."""
    return find_expenses(db, user.user_id, start_date, end_date, category_id)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Eliminar un gasto del usuario (CRUD completo, transaccional)."""
    expense = (
        db.query(Expense)
        .filter(Expense.expense_id == expense_id, Expense.user_id == user.user_id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    db.delete(expense)
    db.commit()
