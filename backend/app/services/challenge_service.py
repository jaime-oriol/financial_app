"""Logica de negocio para challenges.
- Calcula XP server-side (no confiar en cliente).
- Enriquece cada challenge con: best_xp, completed, locked.
- Locked: un challenge de nivel N esta bloqueado si el usuario no ha completado
  al menos UNLOCK_THRESHOLD challenges del nivel N-1. Nivel 1 siempre desbloqueado.
- Orden de salida: por nivel asc, dentro del nivel los no-completados antes que
  los completados, mezclados estable por user_id para sensacion de personalizacion.
"""

import random
from collections import Counter

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.challenge import Challenge, ChallengeAttempt
from app.schemas.challenge import ChallengeResponse


# Nivel N+1 se desbloquea cuando el usuario completa este numero del nivel N.
UNLOCK_THRESHOLD = 3


def list_with_status(db: Session, user_id: int) -> list[ChallengeResponse]:
    """Listar challenges con el progreso real del usuario y los locks."""
    challenges = db.query(Challenge).all()

    best_per_challenge = dict(
        db.query(ChallengeAttempt.challenge_id, func.max(ChallengeAttempt.xp_earned))
        .filter(ChallengeAttempt.user_id == user_id)
        .group_by(ChallengeAttempt.challenge_id)
        .all()
    )

    # Cuantos completados por nivel (necesario para decidir locks)
    completed_by_level: Counter[int] = Counter()
    for c in challenges:
        if c.challenge_id in best_per_challenge:
            completed_by_level[c.level] += 1

    def is_locked(level: int) -> bool:
        if level <= 1:
            return False
        return completed_by_level[level - 1] < UNLOCK_THRESHOLD

    # Shuffle estable por usuario antes de agrupar — pequena variedad personalizada
    rng = random.Random(user_id)
    rng.shuffle(challenges)

    # Orden final: nivel asc, dentro del nivel no-completados antes que completados
    challenges.sort(
        key=lambda c: (c.level, c.challenge_id in best_per_challenge)
    )

    return [
        ChallengeResponse(
            challenge_id=c.challenge_id,
            kind=c.kind,
            title=c.title,
            content=c.content,
            xp_reward=c.xp_reward,
            level=c.level,
            best_xp=best_per_challenge.get(c.challenge_id, 0) or 0,
            completed=c.challenge_id in best_per_challenge,
            locked=is_locked(c.level),
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
