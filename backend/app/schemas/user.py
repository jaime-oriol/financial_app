"""Schemas de usuario: validacion de registro, login y respuesta."""

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


# --- Requests ---

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    birthdate: date
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Responses ---

class UserResponse(BaseModel):
    user_id: int
    name: str
    surname: str
    birthdate: date
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    token: str
    user_id: int
