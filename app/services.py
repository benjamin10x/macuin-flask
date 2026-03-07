from .models import db, Autoparte, Pedido
import json
from datetime import date, datetime

def get_all_autopartes():
    return Autoparte.query.all()

def get_autoparte_by_id(id):
    return Autoparte.query.get_or_404(id)

def create_autoparte(data):
    autoparte = Autoparte(
        nombre=data['nombre'],
        categoria=data['categoria'],
        precio=data['precio'],
        stock=data['stock'],
        descripcion=data.get('descripcion', '')
    )
    db.session.add(autoparte)
    db.session.commit()
    return autoparte

def update_autoparte(autoparte, data):
    autoparte.nombre = data['nombre']
    autoparte.categoria = data['categoria']
    autoparte.precio = data['precio']
    autoparte.stock = data['stock']
    autoparte.descripcion = data.get('descripcion', '')
    db.session.commit()
    return autoparte

def delete_autoparte(autoparte):
    db.session.delete(autoparte)
    db.session.commit()

# Funciones para pedidos
def get_all_pedidos():
    return Pedido.query.order_by(Pedido.fecha.desc()).all()

def get_pedido_by_id(id):
    return Pedido.query.get_or_404(id)

def create_pedido(data):
    # Generar orden_id único
    year = datetime.now().year
    last_pedido = Pedido.query.filter(Pedido.orden_id.like(f'ORD-{year}-%')).order_by(Pedido.id.desc()).first()
    if last_pedido:
        last_num = int(last_pedido.orden_id.split('-')[-1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    orden_id = f'ORD-{year}-{new_num:03d}'
    
    pedido = Pedido(
        orden_id=orden_id,
        cliente=data['cliente'],
        fecha=data.get('fecha', date.today()),
        total=data['total'],
        estado=data.get('estado', 'Recibido'),
        articulos=json.dumps(data['articulos'])
    )
    db.session.add(pedido)
    db.session.commit()
    return pedido

def update_pedido_estado(pedido, estado):
    pedido.estado = estado
    db.session.commit()
    return pedido

def get_pedidos_by_estado():
    estados = ['Recibido', 'Surtido', 'Enviado', 'Entregado']
    return {estado: Pedido.query.filter_by(estado=estado).count() for estado in estados}