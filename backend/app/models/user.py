"""Modelo User: representa un usuario registrado en la aplicacion.
Referencia: Solution Design, ERD p.11, DB Schema p.12 — tabla USERS.
"""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # bcrypt hash
    avatar: Mapped[str | None] = mapped_column(Text, nullable=True)  # base64 data URL de la foto
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )

    # Relaciones 1:N
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    challenge_attempts = relationship("ChallengeAttempt", back_populates="user", cascade="all, delete-orphan")
