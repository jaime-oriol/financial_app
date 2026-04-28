"""Endpoints de metas de ahorro: crear, listar, contribuir, eliminar.
Cumple feedback del profesor: goals deben ser transaccionales (cada accion
modifica la BD).
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.goal import Goal
from app.models.user import User
from app.schemas.goal import GoalContribute, GoalCreate, GoalResponse
from app.services.auth import get_current_user
from app.services.goal_service import build_goal_response, find_goals

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Crear una meta de ahorro nueva."""
    goal = Goal(
        user_id=user.user_id,
        name=data.name,
        target_amount=data.target_amount,
        saved_amount=Decimal("0.00"),
        deadline=data.deadline,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return build_goal_response(goal)


@router.get("", response_model=list[GoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Listar todas las metas del usuario."""
    return find_goals(db, user.user_id)


@router.post("/{goal_id}/contribute", response_model=GoalResponse)
def contribute(
    goal_id: int,
    data: GoalContribute,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Anadir o retirar dinero de una meta. amount puede ser negativo."""
    goal = (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id, Goal.user_id == user.user_id)
        .first()
    )
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    new_saved = goal.saved_amount + data.amount
    if new_saved < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saved amount cannot be negative",
        )

    goal.saved_amount = new_saved
    db.commit()
    db.refresh(goal)
    return build_goal_response(goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Eliminar una meta de ahorro."""
    goal = (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id, Goal.user_id == user.user_id)
        .first()
    )
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    db.delete(goal)
    db.commit()
