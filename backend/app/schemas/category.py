"""Schema de categoria: solo respuesta (las categorias son seeds, no se crean via API)."""

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    category_id: int
    name: str
    icon: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}
