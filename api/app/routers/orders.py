from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import auth, models, schemas

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


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


@router.post("/", status_code=201)
def create_order(
    payload: schemas.CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user),
):
    if not payload.articulos:
        raise HTTPException(400, "El pedido debe tener al menos un artículo.")

    items_data = []
    subtotal = 0.0

    for item in payload.articulos:
        autoparte = db.query(models.Autoparte).filter(
            models.Autoparte.id == item.autoparte_id,
            models.Autoparte.activo == True,
        ).first()
        if not autoparte:
            raise HTTPException(404, f"Autoparte {item.autoparte_id} no encontrada.")
        if autoparte.stock < item.cantidad:
            raise HTTPException(
                400,
                f"Stock insuficiente para '{autoparte.nombre}'. Disponible: {autoparte.stock}",
            )
        linea = round(autoparte.precio * item.cantidad, 2)
        subtotal += linea
        items_data.append({
            "autoparte": autoparte,
            "cantidad": item.cantidad,
            "precio_unitario": autoparte.precio,
            "total_linea": linea,
        })

    subtotal = round(subtotal, 2)
    impuesto = round(subtotal * 0.16, 2)
    total = round(subtotal + impuesto, 2)

    pedido = models.Pedido(
        usuario_id=current_user.id,
        estado="Recibido",
        subtotal=subtotal,
        impuesto=impuesto,
        total=total,
        direccion_envio=payload.direccion_envio,
    )
    db.add(pedido)
    db.flush()

    for d in items_data:
        db.add(models.ArticuloPedido(
            pedido_id=pedido.id,
            autoparte_id=d["autoparte"].id,
            nombre=d["autoparte"].nombre,
            cantidad=d["cantidad"],
            precio_unitario=d["precio_unitario"],
            total_linea=d["total_linea"],
        ))
        d["autoparte"].stock -= d["cantidad"]

    db.commit()
    db.refresh(pedido)
    return _pedido_dict(pedido)


@router.get("/me")
def my_orders(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user),
):
    pedidos = (
        db.query(models.Pedido)
        .filter(models.Pedido.usuario_id == current_user.id)
        .all()
    )
    return [_pedido_dict(p) for p in pedidos]


@router.get("/me/{id}")
def my_order(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user),
):
    p = db.query(models.Pedido).filter(
        models.Pedido.id == id,
        models.Pedido.usuario_id == current_user.id,
    ).first()
    if not p:
        raise HTTPException(404, "Pedido no encontrado.")
    return _pedido_dict(p)
