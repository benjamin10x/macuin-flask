from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import AutoparteForm
from .services import get_all_autopartes, get_autoparte_by_id, create_autoparte, update_autoparte, delete_autoparte, get_all_pedidos, get_pedido_by_id, create_pedido, update_pedido_estado, get_pedidos_by_estado

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("inicio_sesion.html", active_view='login')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validación simple (puedes mejorar esto después)
        if email == 'admin@macuin.com' and password == 'admin123':
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('main.login'))
    
    return render_template("inicio_sesion.html", active_view='login')

@main.route("/dashboard")
def dashboard():
    autopartes = get_all_autopartes()
    total_valor = sum(p.precio * p.stock for p in autopartes)
    bajo_stock = [p for p in autopartes if p.stock < 10]
    return render_template("index.html", autopartes=autopartes, total_valor=total_valor, bajo_stock=bajo_stock)

@main.route("/autopartes")
def autopartes():
    autopartes = get_all_autopartes()
    return render_template("autopartes.html", autopartes=autopartes, active_view='autopartes')

@main.route("/autopartes/nuevo", methods=['GET', 'POST'])
def nuevo_autoparte():
    form = AutoparteForm()
    if form.validate_on_submit():
        data = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'stock': form.stock.data,
            'descripcion': form.descripcion.data
        }
        create_autoparte(data)
        flash('Autoparte creada exitosamente', 'success')
        return redirect(url_for('main.autopartes'))
    return render_template("nuevo_autoparte.html", form=form, active_view='autopartes')

@main.route("/autopartes/<int:id>/editar", methods=['GET', 'POST'])
def editar_autoparte(id):
    autoparte = get_autoparte_by_id(id)
    form = AutoparteForm(obj=autoparte)
    if form.validate_on_submit():
        data = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'stock': form.stock.data,
            'descripcion': form.descripcion.data
        }
        update_autoparte(autoparte, data)
        flash('Autoparte actualizada exitosamente', 'success')
        return redirect(url_for('main.autopartes'))
    return render_template("editar_autoparte.html", form=form, autoparte=autoparte, active_view='autopartes')

@main.route("/autopartes/<int:id>/eliminar", methods=['POST'])
def eliminar_autoparte(id):
    autoparte = get_autoparte_by_id(id)
    delete_autoparte(autoparte)
    flash('Autoparte eliminada exitosamente', 'success')
    return redirect(url_for('main.autopartes'))

@main.route("/inventario")
def inventario():
    autopartes = get_all_autopartes()
    total_valor = sum(p.precio * p.stock for p in autopartes)
    bajo_stock = [p for p in autopartes if p.stock < 10]
    return render_template("inventario.html", autopartes=autopartes, total_valor=total_valor, bajo_stock=bajo_stock, active_view='inventario')

@main.route("/reportes")
def reportes():
    autopartes = get_all_autopartes()
    total_valor = sum(p.precio * p.stock for p in autopartes)
    bajo_stock = [p for p in autopartes if p.stock < 10]
    
    # Group by category
    from collections import Counter
    categorias = list(set(p.categoria for p in autopartes))
    categoria_counts = [Counter(p.categoria for p in autopartes)[cat] for cat in categorias]
    
    return render_template("reportes.html", autopartes=autopartes, total_valor=total_valor, bajo_stock=bajo_stock, categorias=categorias, categoria_counts=categoria_counts, active_view='reportes')

@main.route("/agregar_autoparte", methods=['GET', 'POST'])
def agregar_autoparte():
    form = AutoparteForm()
    if form.validate_on_submit():
        data = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'stock': form.stock.data,
            'descripcion': form.descripcion.data
        }
        create_autoparte(data)
        flash('Autoparte agregada exitosamente', 'success')
        return redirect(url_for('main.autopartes'))
    return render_template("agregar_autoparte.html", form=form, active_view='autopartes')

@main.route("/gestion_pedidos")
def gestion_pedidos():
    pedidos = get_all_pedidos()
    
    # Si no hay pedidos, crear algunos de ejemplo
    if not pedidos:
        from datetime import date, timedelta
        import json
        
        pedidos_ejemplo = [
            {
                'cliente': 'Juan Pérez',
                'fecha': date.today() - timedelta(days=5),
                'articulos': [{'nombre': 'Filtro de aceite', 'cantidad': 2, 'precio': 150}],
                'total': 1340,
                'estado': 'Recibido'
            },
            {
                'cliente': 'María García',
                'fecha': date.today() - timedelta(days=6),
                'articulos': [{'nombre': 'Batería', 'cantidad': 1, 'precio': 2850}],
                'total': 2850,
                'estado': 'Surtido'
            },
            {
                'cliente': 'Carlos López',
                'fecha': date.today() - timedelta(days=7),
                'articulos': [{'nombre': 'Pastillas de freno', 'cantidad': 1, 'precio': 890}],
                'total': 890,
                'estado': 'Enviado'
            },
            {
                'cliente': 'Ana Martínez',
                'fecha': date.today() - timedelta(days=8),
                'articulos': [{'nombre': 'Aceite de motor', 'cantidad': 4, 'precio': 800}],
                'total': 3200,
                'estado': 'Entregado'
            },
            {
                'cliente': 'Roberto Sánchez',
                'fecha': date.today() - timedelta(days=9),
                'articulos': [{'nombre': 'Bujías', 'cantidad': 4, 'precio': 412.5}],
                'total': 1650,
                'estado': 'Recibido'
            },
            {
                'cliente': 'Laura Torres',
                'fecha': date.today() - timedelta(days=10),
                'articulos': [{'nombre': 'Liquido de frenos', 'cantidad': 2, 'precio': 900}],
                'total': 4500,
                'estado': 'Surtido'
            }
        ]
        
        for pedido_data in pedidos_ejemplo:
            create_pedido(pedido_data)
        
        pedidos = get_all_pedidos()
    
    estados_count = get_pedidos_by_estado()
    return render_template("gestion_pedidos.html", pedidos=pedidos, estados_count=estados_count, active_view='pedidos')

@main.route("/pedidos/<int:id>")
def ver_pedido(id):
    pedido = get_pedido_by_id(id)
    return render_template("detalle_pedido.html", pedido=pedido, active_view='pedidos')

@main.route("/pedidos/<int:id>/actualizar_estado", methods=['POST'])
def actualizar_estado_pedido(id):
    pedido = get_pedido_by_id(id)
    nuevo_estado = request.form.get('estado')
    update_pedido_estado(pedido, nuevo_estado)
    flash('Estado del pedido actualizado', 'success')
    return redirect(url_for('main.gestion_pedidos'))

@main.route("/pedidos/nuevo", methods=['GET', 'POST'])
def nuevo_pedido():
    if request.method == 'POST':
        data = {
            'cliente': request.form.get('cliente'),
            'articulos': [],  # Aquí irían los artículos del formulario
            'total': float(request.form.get('total', 0))
        }
        create_pedido(data)
        flash('Pedido creado exitosamente', 'success')
        return redirect(url_for('main.gestion_pedidos'))
    return render_template("nuevo_pedido.html", active_view='pedidos')

@main.route("/inicio_sesion", methods=['GET', 'POST'])
def inicio_sesion():
    return render_template("inicio_sesion.html", active_view='login')

@main.route("/lista_autopartes")
def lista_autopartes():
    autopartes = get_all_autopartes()
    return render_template("lista_autopartes.html", autopartes=autopartes, active_view='autopartes')