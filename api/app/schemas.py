from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ── Autoparte ─────────────────────────────────────────────────────────────────

class AutoparteBase(BaseModel):
    nombre: str
    categoria: str
    precio: float
    stock: int
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    activo: bool = True
    stock_minimo: int = 10


class AutoparteCreate(AutoparteBase):
    pass


class AutoparteUpdate(AutoparteBase):
    pass


class AutoparteOut(AutoparteBase):
    id: int
    fecha_creacion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Usuario / Auth ─────────────────────────────────────────────────────────────

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str] = None
    rol: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioOut


class RegisterRequest(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str


# ── Pedidos ────────────────────────────────────────────────────────────────────

class ArticuloPedidoOut(BaseModel):
    id: int
    autoparte_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    total_linea: float

    model_config = {"from_attributes": True}


class PedidoOut(BaseModel):
    id: int
    orden_id: str
    cliente: str
    email_cliente: str
    fecha: datetime
    estado: str
    subtotal: float
    impuesto: float
    total: float
    direccion_envio: str
    articulos: List[ArticuloPedidoOut] = []

    model_config = {"from_attributes": True}


class ArticuloInput(BaseModel):
    autoparte_id: int
    cantidad: int


class CreateOrderRequest(BaseModel):
    direccion_envio: str
    articulos: List[ArticuloInput]


class UpdateStatusRequest(BaseModel):
    estado: str


# ── Catálogo ───────────────────────────────────────────────────────────────────

class CategoriaOut(BaseModel):
    nombre: str
    total_productos: int
