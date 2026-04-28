"""Logica de negocio para metas de ahorro."""

from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalResponse


def build_goal_response(goal: Goal) -> GoalResponse:
    """Construir response con progreso calculado."""
    progress = (
        float(goal.saved_amount / goal.target_amount * 100)
        if goal.target_amount > 0 else 0.0
    )
    return GoalResponse(
        goal_id=goal.goal_id,
        user_id=goal.user_id,
        name=goal.name,
        target_amount=goal.target_amount,
        saved_amount=goal.saved_amount,
        deadline=goal.deadline,
        created_at=goal.created_at,
        progress=round(min(progress, 100.0), 1),
    )


def find_goals(db: Session, user_id: int) -> list[GoalResponse]:
    goals = (
        db.query(Goal)
        .filter(Goal.user_id == user_id)
        .order_by(Goal.created_at.desc())
        .all()
    )
    return [build_goal_response(g) for g in goals]
