from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserLogin, UserRegister
from app.services.auth import create_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """UC-01: Register account.
    Sequence: validateFields -> findByEmail -> hashPassword -> createUser -> 201 + token.
    """
    # Validar email unico
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    # Crear usuario
    user = User(
        name=data.name,
        surname=data.surname,
        birthdate=data.birthdate,
        email=data.email,
        password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(token=create_token(user.user_id), user_id=user.user_id)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login: validate credentials and return JWT."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenResponse(token=create_token(user.user_id), user_id=user.user_id)
