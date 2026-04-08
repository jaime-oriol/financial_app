"""Endpoints de categorias (solo lectura, las categorias son seeds)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Listar todas las categorias disponibles."""
    return db.query(Category).order_by(Category.category_id).all()
