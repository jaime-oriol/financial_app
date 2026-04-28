"""Punto de entrada de la API. Configura FastAPI, CORS, routers y eventos de inicio."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import auth, budgets, categories, challenges, dashboard, expenses, goals
from app.seed import seed_categories, seed_challenges


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crear tablas, aplicar migraciones idempotentes y ejecutar seeds al arrancar.
    Solo prototipo — en produccion habria que usar Alembic, pero aqui usamos
    ALTER TABLE IF NOT EXISTS para no romper despliegues con tabla existente.
    """
    Base.metadata.create_all(bind=engine)
    _apply_inline_migrations()
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_challenges(db)
    finally:
        db.close()
    yield


def _apply_inline_migrations() -> None:
    """ALTER TABLE idempotente para columnas anadidas tras el create_all inicial.
    Solo en Postgres — SQLite (tests) parte de tabla limpia con todas las columnas.
    """
    if engine.dialect.name != "postgresql":
        return
    statements = [
        # Avatar: anadir si falta, ampliar tipo a TEXT (antes VARCHAR(8) para emoji)
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar TEXT",
        "ALTER TABLE users ALTER COLUMN avatar TYPE TEXT",
        # Level en challenges (default 1)
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS level INTEGER NOT NULL DEFAULT 1",
    ]
    for sql in statements:
        try:
            with engine.begin() as conn:
                conn.exec_driver_sql(sql)
        except Exception as exc:  # noqa: BLE001 — pragmatico, no debe tirar el server
            print(f"[migration skipped] {sql} -> {exc}")


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
app.include_router(goals.router, prefix="/api")
app.include_router(challenges.router, prefix="/api")


@app.get("/health")
def health():
    """Health check para verificar que el servidor esta activo."""
    return {"status": "ok"}
