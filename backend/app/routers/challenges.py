"""Endpoints de challenges (quiz + simulation).
Listar retos disponibles con estado del usuario y registrar intentos
(transaccional: la respuesta queda almacenada en BD).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.challenge import Challenge, ChallengeAttempt
from app.models.user import User
from app.schemas.challenge import AttemptCreate, AttemptResponse, ChallengeResponse
from app.services.auth import get_current_user
from app.services.challenge_service import compute_xp, list_with_status

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("", response_model=list[ChallengeResponse])
def get_challenges(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Listar retos disponibles con el estado del usuario (mejor XP, completado)."""
    return list_with_status(db, user.user_id)


@router.post("/{challenge_id}/attempt", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
def submit_attempt(
    challenge_id: int,
    data: AttemptCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Registrar un intento. XP se calcula server-side segun tipo y payload."""
    challenge = db.query(Challenge).filter(Challenge.challenge_id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")

    xp = compute_xp(challenge, data.payload)
    attempt = ChallengeAttempt(
        user_id=user.user_id,
        challenge_id=challenge_id,
        payload=data.payload,
        xp_earned=xp,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt
