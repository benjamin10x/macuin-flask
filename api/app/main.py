import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, admin, catalog, orders
from app import seed

# Crear directorio de datos si no existe (para SQLite)
os.makedirs("/data", exist_ok=True)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MACUIN API",
    version="2.0.0",
    description="API REST del sistema de autopartes MACUIN",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(catalog.router)
app.include_router(orders.router)


@app.on_event("startup")
def on_startup() -> None:
    seed.run_seed()


@app.get("/")
def root():
    return {"status": "ok", "version": "2.0.0"}
