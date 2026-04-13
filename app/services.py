from __future__ import annotations

from datetime import datetime

import requests
from flask import current_app

from .models import ArticuloPedido, Autoparte, Pedido


class ApiError(RuntimeError):
    pass


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _build_url(path: str) -> str:
    base = current_app.config["API_BASE_URL"].rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def _request(method: str, path: str, token: str | None = None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.request(
        method,
        _build_url(path),
        headers=headers,
        timeout=current_app.config["API_TIMEOUT"],
        **kwargs,
    )
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise ApiError(detail or "Error al comunicarse con la API.")
    if response.status_code == 204:
        return None
    return response.json()


def _map_autoparte(payload: dict) -> Autoparte:
    return Autoparte(
        id=payload["id"],
        nombre=payload["nombre"],
        categoria=payload["categoria"],
        precio=float(payload["precio"]),
        stock=int(payload["stock"]),
        descripcion=payload.get("descripcion"),
        marca=payload.get("marca"),
        activo=payload.get("activo", True),
        stock_minimo=int(payload.get("stock_minimo", 10)),
        fecha_creacion=_parse_datetime(payload.get("fecha_creacion")),
    )


def _map_articulo(payload: dict) -> ArticuloPedido:
    return ArticuloPedido(
        id=payload["id"],
        autoparte_id=payload["autoparte_id"],
        nombre=payload["nombre"],
        cantidad=payload["cantidad"],
        precio_unitario=float(payload["precio_unitario"]),
        total_linea=float(payload["total_linea"]),
    )


def _map_pedido(payload: dict) -> Pedido:
    return Pedido(
        id=payload["id"],
        orden_id=payload["orden_id"],
        cliente=payload["cliente"],
        email_cliente=payload["email_cliente"],
        fecha=_parse_datetime(payload["fecha"]),
        estado=payload["estado"],
        subtotal=float(payload["subtotal"]),
        impuesto=float(payload["impuesto"]),
        total=float(payload["total"]),
        direccion_envio=payload["direccion_envio"],
        articulos=[_map_articulo(item) for item in payload.get("articulos", [])],
    )


def login_internal_user(email: str, password: str) -> dict:
    payload = _request(
        "POST",
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if payload["user"]["rol"] != "admin":
        raise ApiError("La cuenta no tiene permisos de administrador.")
    return payload


def get_dashboard_data(token: str) -> dict:
    return _request("GET", "/admin/dashboard", token=token)


def get_all_autopartes(token: str) -> list[Autoparte]:
    payload = _request("GET", "/admin/products", token=token)
    return [_map_autoparte(item) for item in payload]


def get_autoparte_by_id(token: str, autoparte_id: int) -> Autoparte:
    payload = _request("GET", f"/admin/products/{autoparte_id}", token=token)
    return _map_autoparte(payload)


def create_autoparte(token: str, data: dict) -> Autoparte:
    payload = _request("POST", "/admin/products", token=token, json=data)
    return _map_autoparte(payload)


def update_autoparte(token: str, autoparte_id: int, data: dict) -> Autoparte:
    payload = _request("PUT", f"/admin/products/{autoparte_id}", token=token, json=data)
    return _map_autoparte(payload)


def delete_autoparte(token: str, autoparte_id: int) -> None:
    _request("DELETE", f"/admin/products/{autoparte_id}", token=token)


def get_all_pedidos(token: str) -> list[Pedido]:
    payload = _request("GET", "/admin/orders", token=token)
    return [_map_pedido(item) for item in payload]


def get_pedido_by_id(token: str, pedido_id: int) -> Pedido:
    payload = _request("GET", f"/admin/orders/{pedido_id}", token=token)
    return _map_pedido(payload)


def update_pedido_estado(token: str, pedido_id: int, estado: str) -> Pedido:
    payload = _request(
        "PATCH",
        f"/admin/orders/{pedido_id}/status",
        token=token,
        json={"estado": estado},
    )
    return _map_pedido(payload)


def get_pedidos_by_estado(token: str) -> dict[str, int]:
    dashboard = get_dashboard_data(token)
    conteo = dashboard.get("conteo_estados", {})
    return {
        "Recibido": conteo.get("Recibido", 0),
        "Surtido": conteo.get("Surtido", 0),
        "Enviado": conteo.get("Enviado", 0),
        "Entregado": conteo.get("Entregado", 0),
    }
