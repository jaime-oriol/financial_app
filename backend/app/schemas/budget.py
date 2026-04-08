"""Schemas de presupuestos: validacion de creacion y respuesta con progreso."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# --- Requests ---

class BudgetCreate(BaseModel):
    category_id: int
    limit_amount: Decimal = Field(gt=0)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2020)


# --- Responses ---

class BudgetResponse(BaseModel):
    budget_id: int
    user_id: int
    category_id: int
    month: int
    year: int
    limit_amount: Decimal
    created_at: datetime
    category_name: str | None = None
    spent: Decimal = Decimal("0.00")
    progress: float = 0.0

    model_config = {"from_attributes": True}
