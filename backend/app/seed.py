"""Seed de categorias iniciales. Se ejecuta al arrancar si la tabla esta vacia."""

from sqlalchemy.orm import Session

from app.models.category import Category

INITIAL_CATEGORIES = [
    {"name": "Food", "icon": "restaurant", "description": "Meals, groceries and snacks"},
    {"name": "Transport", "icon": "directions_bus", "description": "Bus, metro, gas and rides"},
    {"name": "Entertainment", "icon": "movie", "description": "Movies, games and outings"},
    {"name": "Health", "icon": "local_hospital", "description": "Medical, pharmacy and wellness"},
    {"name": "Education", "icon": "school", "description": "Books, courses and supplies"},
    {"name": "Other", "icon": "more_horiz", "description": "Miscellaneous expenses"},
]


def seed_categories(db: Session) -> None:
    """Insertar categorias solo si la tabla esta vacia."""
    if db.query(Category).count() > 0:
        return

    for cat_data in INITIAL_CATEGORIES:
        db.add(Category(**cat_data))
    db.commit()
