"""Logica de negocio para challenges. Calcula XP server-side (no confiar en cliente)
y enriquece challenges con el mejor intento del usuario.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.challenge import Challenge, ChallengeAttempt
from app.schemas.challenge import ChallengeResponse


def list_with_status(db: Session, user_id: int) -> list[ChallengeResponse]:
    """Listar todos los challenges con el mejor intento del usuario."""
    challenges = db.query(Challenge).order_by(Challenge.challenge_id).all()
    best_per_challenge = dict(
        db.query(ChallengeAttempt.challenge_id, func.max(ChallengeAttempt.xp_earned))
        .filter(ChallengeAttempt.user_id == user_id)
        .group_by(ChallengeAttempt.challenge_id)
        .all()
    )
    return [
        ChallengeResponse(
            challenge_id=c.challenge_id,
            kind=c.kind,
            title=c.title,
            content=c.content,
            xp_reward=c.xp_reward,
            best_xp=best_per_challenge.get(c.challenge_id, 0) or 0,
            completed=c.challenge_id in best_per_challenge,
        )
        for c in challenges
    ]


def compute_xp(challenge: Challenge, payload: dict) -> int:
    """Calcular XP server-side segun tipo. Cliente no decide su recompensa."""
    if challenge.kind == "quiz":
        score = int(payload.get("score", 0))
        return max(score, 0) * 10
    if challenge.kind == "simulation":
        idx = int(payload.get("choice_idx", -1))
        choices = challenge.content.get("choices", [])
        if 0 <= idx < len(choices):
            return int(choices[idx].get("xp", 0))
    return 0


def total_xp(db: Session, user_id: int) -> int:
    """Suma de XP ganado por un usuario en todos sus intentos."""
    result = (
        db.query(func.coalesce(func.sum(ChallengeAttempt.xp_earned), 0))
        .filter(ChallengeAttempt.user_id == user_id)
        .scalar()
    )
    return int(result or 0)


def attempt_count(db: Session, user_id: int) -> int:
    """Numero total de intentos del usuario."""
    return (
        db.query(func.count(ChallengeAttempt.attempt_id))
        .filter(ChallengeAttempt.user_id == user_id)
        .scalar()
    ) or 0
