"""Modelos Challenge y ChallengeAttempt: retos transaccionales (quiz + simulation).
Cumple feedback del profesor: las respuestas se almacenan en BD, nada hardcoded.
Contenido del reto en columna JSON (questions / scenario+choices) — flexible.
"""

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Challenge(Base):
    __tablename__ = "challenges"

    challenge_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)  # 'quiz' | 'simulation'
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 1=Beginner, 2=Intermediate, 3=Advanced

    attempts = relationship("ChallengeAttempt", back_populates="challenge", cascade="all, delete-orphan")


class ChallengeAttempt(Base):
    __tablename__ = "challenge_attempts"

    attempt_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    challenge_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("challenges.challenge_id"), nullable=False
    )
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)  # {score, total} o {choice_idx}
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="challenge_attempts")
    challenge = relationship("Challenge", back_populates="attempts")
