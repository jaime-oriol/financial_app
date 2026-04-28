"""Schemas de challenges (quiz + simulation) y attempts del usuario."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ChallengeResponse(BaseModel):
    """Reto disponible. content varia por kind:
    - kind='quiz': content = {questions: [{question, options, correct, explanation}, ...]}
    - kind='simulation': content = {scenario, budget, choices: [{label, split, tag, outcome, savings, xp}, ...]}
    """
    challenge_id: int
    kind: str
    title: str
    content: dict[str, Any]
    xp_reward: int
    best_xp: int = 0  # Mejor XP del usuario en este reto
    completed: bool = False  # Si el usuario ya hizo al menos un intento

    model_config = {"from_attributes": True}


class AttemptCreate(BaseModel):
    """Body para POST /challenges/{id}/attempt.
    payload varia por kind: quiz -> {score, total}; simulation -> {choice_idx}.
    """
    payload: dict[str, Any]


class AttemptResponse(BaseModel):
    attempt_id: int
    challenge_id: int
    payload: dict[str, Any]
    xp_earned: int
    created_at: datetime

    model_config = {"from_attributes": True}
