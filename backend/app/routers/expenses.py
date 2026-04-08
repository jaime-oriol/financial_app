from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """UC-02: Add expense (manual).
    Sequence: validateAmount -> findCategoryById -> insertExpense -> updateBalance -> 201.
    """
    # Validar que la categoria existe
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

    return ExpenseResponse(
        expense_id=expense.expense_id,
        user_id=expense.user_id,
        category_id=expense.category_id,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        created_at=expense.created_at,
        category_name=category.name,
    )


@router.get("", response_model=list[ExpenseResponse])
def get_expenses(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    category_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """UC-04: View expense history.
    Sequence: findExpenses(userId, filters) -> 200 + expenses[] | empty hint.
    """
    query = db.query(Expense).filter(Expense.user_id == user.user_id)

    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    if category_id:
        query = query.filter(Expense.category_id == category_id)

    expenses = query.order_by(Expense.expense_date.desc()).all()

    result = []
    for e in expenses:
        cat = db.query(Category).filter(Category.category_id == e.category_id).first()
        result.append(
            ExpenseResponse(
                expense_id=e.expense_id,
                user_id=e.user_id,
                category_id=e.category_id,
                amount=e.amount,
                description=e.description,
                expense_date=e.expense_date,
                created_at=e.created_at,
                category_name=cat.name if cat else None,
            )
        )
    return result
