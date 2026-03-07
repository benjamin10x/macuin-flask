from . import db

class Autoparte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.Text)

    def __repr__(self):
        return f'<Autoparte {self.nombre}>'

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.String(20), unique=True, nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Recibido')
    articulos = db.Column(db.Text, nullable=False)  # JSON string de artículos
    
    def __repr__(self):
        return f'<Pedido {self.orden_id}>'