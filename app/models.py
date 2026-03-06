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