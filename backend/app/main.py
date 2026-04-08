"""Punto de entrada de la API. Configura FastAPI, routers y eventos de inicio."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.routers import auth, budgets, categories, dashboard, expenses
from app.seed import seed_categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas y ejecutar seeds al arrancar
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_categories(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="FAPP — Financial App",
    description="API for teen financial literacy app",
    version="1.0.0",
    lifespan=lifespan,
)

# Registrar routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
