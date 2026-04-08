from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    category_id: int
    name: str
    icon: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}
