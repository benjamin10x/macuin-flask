import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


def _gen_orden_id() -> str:
    return f"ORD-{str(uuid.uuid4())[:8].upper()}"


class Autoparte(Base):
    __tablename__ = "autopartes"

    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(200), nullable=False)
    categoria      = Column(String(100), nullable=False)
    precio         = Column(Float, nullable=False)
    stock          = Column(Integer, default=0, nullable=False)
    descripcion    = Column(Text, nullable=True)
    marca          = Column(String(100), nullable=True)
    activo         = Column(Boolean, default=True, nullable=False)
    stock_minimo   = Column(Integer, default=10, nullable=False)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    articulos = relationship("ArticuloPedido", back_populates="autoparte")


class Usuario(Base):
    __tablename__ = "usuarios"

    id            = Column(Integer, primary_key=True, index=True)
    nombre        = Column(String(200), nullable=False)
    email         = Column(String(200), unique=True, nullable=False, index=True)
    telefono      = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    rol           = Column(String(20), default="cliente", nullable=False)

    pedidos = relationship("Pedido", back_populates="usuario")


class Pedido(Base):
    __tablename__ = "pedidos"

    id             = Column(Integer, primary_key=True, index=True)
    orden_id       = Column(String(50), unique=True, nullable=False, default=_gen_orden_id)
    usuario_id     = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado         = Column(String(30), default="Recibido", nullable=False)
    subtotal       = Column(Float, default=0.0, nullable=False)
    impuesto       = Column(Float, default=0.0, nullable=False)
    total          = Column(Float, default=0.0, nullable=False)
    direccion_envio = Column(String(500), nullable=False)
    fecha          = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario   = relationship("Usuario", back_populates="pedidos")
    articulos = relationship("ArticuloPedido", back_populates="pedido")


class ArticuloPedido(Base):
    __tablename__ = "articulos_pedido"

    id             = Column(Integer, primary_key=True, index=True)
    pedido_id      = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    autoparte_id   = Column(Integer, ForeignKey("autopartes.id"), nullable=False)
    nombre         = Column(String(200), nullable=False)
    cantidad       = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total_linea    = Column(Float, nullable=False)

    pedido    = relationship("Pedido", back_populates="articulos")
    autoparte = relationship("Autoparte", back_populates="articulos")
