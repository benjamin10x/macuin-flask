from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import auth, models, schemas

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


# ── Helpers ───────────────────────────────────────────────────────────────────

def _pedido_dict(p: models.Pedido) -> dict:
    return {
        "id": p.id,
        "orden_id": p.orden_id,
        "cliente": p.usuario.nombre,
        "email_cliente": p.usuario.email,
        "fecha": p.fecha.isoformat(),
        "estado": p.estado,
        "subtotal": p.subtotal,
        "impuesto": p.impuesto,
        "total": p.total,
        "direccion_envio": p.direccion_envio,
        "articulos": [
            {
                "id": a.id,
                "autoparte_id": a.autoparte_id,
                "nombre": a.nombre,
                "cantidad": a.cantidad,
                "precio_unitario": a.precio_unitario,
                "total_linea": a.total_linea,
            }
            for a in p.articulos
        ],
    }


# ── Dashboard ─────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    autopartes = db.query(models.Autoparte).all()
    bajo_stock = [a for a in autopartes if a.stock <= a.stock_minimo]
    total_valor = sum(a.precio * a.stock for a in autopartes)

    pedidos = db.query(models.Pedido).all()
    conteo: dict[str, int] = {}
    for p in pedidos:
        conteo[p.estado] = conteo.get(p.estado, 0) + 1

    return {
        "autopartes": [schemas.AutoparteOut.model_validate(a).model_dump() for a in autopartes],
        "total_valor_inventario": total_valor,
        "productos_bajo_stock": [schemas.AutoparteOut.model_validate(a).model_dump() for a in bajo_stock],
        "conteo_estados": {
            "Recibido":  conteo.get("Recibido", 0),
            "Surtido":   conteo.get("Surtido", 0),
            "Enviado":   conteo.get("Enviado", 0),
            "Entregado": conteo.get("Entregado", 0),
        },
        "total_pedidos": len(pedidos),
    }


# ── Autopartes (CRUD) ─────────────────────────────────────────────────────────

@router.get("/products", response_model=List[schemas.AutoparteOut])
def list_products(
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    return db.query(models.Autoparte).all()


@router.get("/products/{id}", response_model=schemas.AutoparteOut)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    a = db.query(models.Autoparte).filter(models.Autoparte.id == id).first()
    if not a:
        raise HTTPException(404, "Autoparte no encontrada.")
    return a


@router.post("/products", response_model=schemas.AutoparteOut, status_code=201)
def create_product(
    payload: schemas.AutoparteCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    a = models.Autoparte(**payload.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.put("/products/{id}", response_model=schemas.AutoparteOut)
def update_product(
    id: int,
    payload: schemas.AutoparteUpdate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    a = db.query(models.Autoparte).filter(models.Autoparte.id == id).first()
    if not a:
        raise HTTPException(404, "Autoparte no encontrada.")
    for k, v in payload.model_dump().items():
        setattr(a, k, v)
    db.commit()
    db.refresh(a)
    return a


@router.delete("/products/{id}", status_code=204)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    a = db.query(models.Autoparte).filter(models.Autoparte.id == id).first()
    if not a:
        raise HTTPException(404, "Autoparte no encontrada.")
    db.delete(a)
    db.commit()


# ── Pedidos ───────────────────────────────────────────────────────────────────

@router.get("/orders")
def list_orders(
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    return [_pedido_dict(p) for p in db.query(models.Pedido).all()]


@router.get("/orders/{id}")
def get_order(
    id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    p = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not p:
        raise HTTPException(404, "Pedido no encontrado.")
    return _pedido_dict(p)


@router.patch("/orders/{id}/status")
def update_order_status(
    id: int,
    payload: schemas.UpdateStatusRequest,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.require_admin),
):
    VALID = {"Recibido", "Surtido", "Enviado", "Entregado", "Cancelado"}
    if payload.estado not in VALID:
        raise HTTPException(400, f"Estado inválido. Valores permitidos: {', '.join(sorted(VALID))}")
    p = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not p:
        raise HTTPException(404, "Pedido no encontrado.")
    p.estado = payload.estado
    db.commit()
    db.refresh(p)
    return _pedido_dict(p)
