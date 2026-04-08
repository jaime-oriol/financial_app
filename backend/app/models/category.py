"""Modelo Category: tipos de gasto predefinidos (seeds).
Referencia: Solution Design, ERD p.11, DB Schema p.12 — tabla CATEGORY.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relaciones 1:N con gastos y presupuestos
    expenses = relationship("Expense", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
