"""Punto de entrada de la API. Configura FastAPI, CORS, routers y eventos de inicio."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import auth, budgets, categories, dashboard, expenses
from app.seed import seed_categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crear tablas y ejecutar seeds al arrancar (solo prototipo, en produccion usar Alembic)."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_categories(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="FAPP — Financial App",
    description="REST API for teen financial literacy app (3:2 Analytics)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: permitir requests desde el frontend Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En produccion, restringir al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers con prefijo /api
app.include_router(auth.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(budgets.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/health")
def health():
    """Health check para verificar que el servidor esta activo."""
    return {"status": "ok"}
