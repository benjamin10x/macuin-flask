from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/v1/catalog", tags=["Catalog"])


@router.get("/summary")
def catalog_summary(db: Session = Depends(get_db)):
    autopartes = db.query(models.Autoparte).filter(models.Autoparte.activo == True).all()

    cat_count: dict[str, int] = {}
    for a in autopartes:
        cat_count[a.categoria] = cat_count.get(a.categoria, 0) + 1
    categorias = [{"nombre": k, "total_productos": v} for k, v in cat_count.items()]

    destacados = [a for a in autopartes if a.stock > 0][:4]
    total_clientes = db.query(models.Usuario).filter(models.Usuario.rol == "cliente").count()

    return {
        "categorias": categorias,
        "destacados": [schemas.AutoparteOut.model_validate(a).model_dump() for a in destacados],
        "total_productos": len(autopartes),
        "total_clientes": total_clientes,
        "tiempo_entrega_horas": 24,
    }


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    autopartes = db.query(models.Autoparte).filter(models.Autoparte.activo == True).all()
    cat_count: dict[str, int] = {}
    for a in autopartes:
        cat_count[a.categoria] = cat_count.get(a.categoria, 0) + 1
    return [{"nombre": k, "total_productos": v} for k, v in cat_count.items()]


@router.get("/products")
def list_products(search: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.Autoparte).filter(models.Autoparte.activo == True)
    if search:
        term = f"%{search}%"
        q = q.filter(
            models.Autoparte.nombre.ilike(term)
            | models.Autoparte.categoria.ilike(term)
            | models.Autoparte.descripcion.ilike(term)
        )
    return [schemas.AutoparteOut.model_validate(a).model_dump() for a in q.all()]


@router.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    a = db.query(models.Autoparte).filter(
        models.Autoparte.id == id,
        models.Autoparte.activo == True,
    ).first()
    if not a:
        raise HTTPException(404, "Producto no encontrado.")
    return schemas.AutoparteOut.model_validate(a).model_dump()
