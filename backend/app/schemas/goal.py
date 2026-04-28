"""Schemas de metas de ahorro: creacion, contribucion y respuesta con progreso."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# --- Requests ---

class GoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: Decimal = Field(gt=0)
    deadline: date | None = None


class GoalContribute(BaseModel):
    amount: Decimal  # Puede ser negativo para retirar


# --- Responses ---

class GoalResponse(BaseModel):
    goal_id: int
    user_id: int
    name: str
    target_amount: Decimal
    saved_amount: Decimal
    deadline: date | None
    created_at: datetime
    progress: float = 0.0  # % de target alcanzado

    model_config = {"from_attributes": True}
