from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    # IMPORTAR MODELOS
    from .models import Autoparte, Pedido

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app