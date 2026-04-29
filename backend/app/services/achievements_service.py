"""Achievements: badges 100% derivados de la BD del usuario.
Sin nada hardcoded — cada criterio es una query real:
- First Saver: tiene al menos un goal con saved_amount > 0
- Hot Streak: streak (calculado) >= 7
- Budget Pro: tiene presupuesto y al menos un gasto registrado
- Quiz Master: ha conseguido la maxima XP en algun quiz
- Goal Crusher: ha completado al menos una meta (saved >= target)
"""

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.challenge import Challenge, ChallengeAttempt
from app.models.expense import Expense
from app.models.goal import Goal


# Metadata de los achievements (UI: nombre, icono, color, descripcion).
# El campo `earned` se calcula por usuario.
_DEFINITIONS = [
    {
        "id": "first_saver",
        "name": "First Saver",
        "icon": "savings",
        "color": "#27AE60",
        "description": "Contributed to a savings goal for the first time",
    },
    {
        "id": "hot_streak",
        "name": "Hot Streak",
        "icon": "local_fire_department",
        "color": "#F39C12",
        "description": "Tracked expenses for 7 consecutive days",
    },
    {
        "id": "budget_pro",
        "name": "Budget Pro",
        "icon": "account_balance_wallet",
        "color": "#2675E3",
        "description": "Set up a budget and recorded at least one expense",
    },
    {
        "id": "quiz_master",
        "name": "Quiz Master",
        "icon": "emoji_events",
        "color": "#8E44AD",
        "description": "Achieved a perfect score on a quiz",
    },
    {
        "id": "goal_crusher",
        "name": "Goal Achiever",
        "icon": "flag",
        "color": "#E74C3C",
        "description": "Reached a savings goal target",
    },
]


def compute_achievements(db: Session, user_id: int, streak: int) -> list[dict]:
    """Calcular que achievements ha conseguido el usuario. Cada criterio
    consulta la BD — nada hardcoded."""
    first_saver = (
        db.query(Goal)
        .filter(Goal.user_id == user_id, Goal.saved_amount > 0)
        .first()
        is not None
    )

    hot_streak = streak >= 7

    has_budget = (
        db.query(Budget).filter(Budget.user_id == user_id).first() is not None
    )
    has_expense = (
        db.query(Expense).filter(Expense.user_id == user_id).first() is not None
    )
    budget_pro = has_budget and has_expense

    quiz_master = (
        db.query(ChallengeAttempt)
        .join(Challenge, Challenge.challenge_id == ChallengeAttempt.challenge_id)
        .filter(
            ChallengeAttempt.user_id == user_id,
            Challenge.kind == "quiz",
            ChallengeAttempt.xp_earned >= Challenge.xp_reward,
        )
        .first()
        is not None
    )

    goal_crusher = (
        db.query(Goal)
        .filter(Goal.user_id == user_id, Goal.saved_amount >= Goal.target_amount)
        .first()
        is not None
    )

    earned_by_id = {
        "first_saver": first_saver,
        "hot_streak": hot_streak,
        "budget_pro": budget_pro,
        "quiz_master": quiz_master,
        "goal_crusher": goal_crusher,
    }

    return [{**defn, "earned": earned_by_id[defn["id"]]} for defn in _DEFINITIONS]
