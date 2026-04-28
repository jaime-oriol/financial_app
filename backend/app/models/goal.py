"""Modelo Goal: meta de ahorro del usuario.
Cumple feedback del profesor: goals deben ser transaccionales (botones +/- para
meter/sacar dinero). saved_amount se actualiza via POST /goals/{id}/contribute.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    goal_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    saved_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="goals")
