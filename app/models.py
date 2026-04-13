from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Autoparte:
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int
    descripcion: str | None = None
    marca: str | None = None
    activo: bool = True
    stock_minimo: int = 10
    fecha_creacion: datetime | None = None


@dataclass
class ArticuloPedido:
    id: int
    autoparte_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    total_linea: float


@dataclass
class Pedido:
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
    articulos: list[ArticuloPedido] = field(default_factory=list)
