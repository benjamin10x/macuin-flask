from .models import db, Autoparte

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