"""Schemas de gastos: validacion de creacion y formato de respuesta."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# --- Requests ---

class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    description: str = Field(max_length=255, default="No description")
    expense_date: date
    category_id: int


# --- Responses ---

class ExpenseResponse(BaseModel):
    expense_id: int
    user_id: int
    category_id: int
    amount: Decimal
    description: str
    expense_date: date
    created_at: datetime
    category_name: str | None = None

    model_config = {"from_attributes": True}
