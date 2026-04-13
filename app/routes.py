from collections import Counter
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .forms import AutoparteForm
from .services import (
    ApiError,
    create_autoparte,
    delete_autoparte,
    get_all_autopartes,
    get_all_pedidos,
    get_autoparte_by_id,
    get_dashboard_data,
    get_pedido_by_id,
    get_pedidos_by_estado,
    login_internal_user,
    update_autoparte,
    update_pedido_estado,
)

main = Blueprint("main", __name__)


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped_view


def _access_token() -> str:
    return session["access_token"]


def _autoparte_payload(form: AutoparteForm) -> dict:
    return {
        "nombre": form.nombre.data,
        "categoria": form.categoria.data,
        "precio": form.precio.data,
        "stock": form.stock.data,
        "descripcion": form.descripcion.data,
        "marca": None,
        "stock_minimo": 10,
        "activo": True,
    }

@main.route("/")
def index():
    if session.get("access_token"):
        return redirect(url_for("main.dashboard"))
    return render_template("inicio_sesion.html", active_view='login')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("access_token"):
        return redirect(url_for("main.dashboard"))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            auth = login_internal_user(email, password)
        except ApiError as exc:
            flash(str(exc), "error")
            return render_template("inicio_sesion.html", active_view="login")

        session["access_token"] = auth["access_token"]
        session["user"] = auth["user"]
        flash("Inicio de sesion exitoso", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("inicio_sesion.html", active_view='login')

@main.route("/logout", methods=["POST"])
@admin_required
def logout():
    session.clear()
    return redirect(url_for("main.login"))

@main.route("/dashboard")
@admin_required
def dashboard():
    try:
        payload = get_dashboard_data(_access_token())
    except ApiError as exc:
        flash(str(exc), "error")
        return redirect(url_for("main.login"))
    return render_template(
        "index.html",
        autopartes=payload.get("autopartes", []),
        total_valor=payload.get("total_valor_inventario", 0),
        bajo_stock=payload.get("productos_bajo_stock", []),
    )

@main.route("/autopartes")
@admin_required
def autopartes():
    try:
        autopartes = get_all_autopartes(_access_token())
    except ApiError as exc:
        flash(str(exc), 'error')
        autopartes = []
    return render_template("autopartes.html", autopartes=autopartes, active_view='autopartes')

@main.route("/autopartes/nuevo", methods=['GET', 'POST'])
@admin_required
def nuevo_autoparte():
    form = AutoparteForm()
    if form.validate_on_submit():
        try:
            create_autoparte(_access_token(), _autoparte_payload(form))
            flash('Autoparte creada exitosamente.', 'success')
            return redirect(url_for('main.autopartes'))
        except ApiError as exc:
            flash(str(exc), 'error')
    return render_template("nuevo_autoparte.html", form=form, active_view='autopartes')

@main.route("/autopartes/<int:id>/editar", methods=['GET', 'POST'])
@admin_required
def editar_autoparte(id):
    try:
        autoparte = get_autoparte_by_id(_access_token(), id)
    except ApiError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('main.autopartes'))
    form = AutoparteForm(obj=autoparte)
    if form.validate_on_submit():
        try:
            update_autoparte(_access_token(), autoparte.id, _autoparte_payload(form))
            flash('Autoparte actualizada exitosamente.', 'success')
            return redirect(url_for('main.autopartes'))
        except ApiError as exc:
            flash(str(exc), 'error')
    return render_template("editar_autoparte.html", form=form, autoparte=autoparte, active_view='autopartes')

@main.route("/autopartes/<int:id>/eliminar", methods=['POST'])
@admin_required
def eliminar_autoparte(id):
    try:
        delete_autoparte(_access_token(), id)
        flash('Autoparte eliminada exitosamente.', 'success')
    except ApiError as exc:
        flash(str(exc), 'error')
    return redirect(url_for('main.autopartes'))

@main.route("/inventario")
@admin_required
def inventario():
    try:
        autopartes = get_all_autopartes(_access_token())
    except ApiError as exc:
        flash(str(exc), 'error')
        autopartes = []
    total_valor = sum(p.precio * p.stock for p in autopartes)
    bajo_stock = [p for p in autopartes if p.stock <= p.stock_minimo]
    return render_template("inventario.html", autopartes=autopartes, total_valor=total_valor, bajo_stock=bajo_stock, active_view='inventario')

@main.route("/reportes")
@admin_required
def reportes():
    try:
        autopartes = get_all_autopartes(_access_token())
    except ApiError as exc:
        flash(str(exc), 'error')
        autopartes = []
    total_valor = sum(p.precio * p.stock for p in autopartes)
    bajo_stock = [p for p in autopartes if p.stock <= p.stock_minimo]
    categorias_counter = Counter(p.categoria for p in autopartes)
    return render_template(
        "reportes.html",
        autopartes=autopartes,
        total_valor=total_valor,
        bajo_stock=bajo_stock,
        categorias=list(categorias_counter.keys()),
        categoria_counts=list(categorias_counter.values()),
        active_view='reportes',
    )

@main.route("/agregar_autoparte", methods=['GET', 'POST'])
@admin_required
def agregar_autoparte():
    return redirect(url_for("main.nuevo_autoparte"))

@main.route("/gestion_pedidos")
@admin_required
def gestion_pedidos():
    try:
        pedidos = get_all_pedidos(_access_token())
        estados_count = get_pedidos_by_estado(_access_token())
    except ApiError as exc:
        flash(str(exc), 'error')
        pedidos = []
        estados_count = {'Recibido': 0, 'Surtido': 0, 'Enviado': 0, 'Entregado': 0}
    return render_template("gestion_pedidos.html", pedidos=pedidos, estados_count=estados_count, active_view='pedidos')

@main.route("/pedidos/<int:id>")
@admin_required
def ver_pedido(id):
    try:
        pedido = get_pedido_by_id(_access_token(), id)
    except ApiError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('main.gestion_pedidos'))
    return render_template("detalle_pedido.html", pedido=pedido, active_view='pedidos')

@main.route("/pedidos/<int:id>/actualizar_estado", methods=['POST'])
@admin_required
def actualizar_estado_pedido(id):
    nuevo_estado = request.form.get('estado')
    ESTADOS_VALIDOS = ['Recibido', 'Surtido', 'Enviado', 'Entregado', 'Cancelado']
    if not nuevo_estado or nuevo_estado not in ESTADOS_VALIDOS:
        flash('Estado inválido.', 'error')
        return redirect(url_for('main.ver_pedido', id=id))
    try:
        update_pedido_estado(_access_token(), id, nuevo_estado)
        flash('Estado del pedido actualizado correctamente.', 'success')
    except ApiError as exc:
        flash(str(exc), 'error')
    return redirect(url_for('main.ver_pedido', id=id))

@main.route("/pedidos/nuevo", methods=['GET', 'POST'])
@admin_required
def nuevo_pedido():
    return redirect(url_for("main.gestion_pedidos"))

@main.route("/inicio_sesion", methods=['GET', 'POST'])
def inicio_sesion():
    if session.get("access_token"):
        return redirect(url_for("main.dashboard"))
    return render_template("inicio_sesion.html", active_view='login')

@main.route("/lista_autopartes")
@admin_required
def lista_autopartes():
    return redirect(url_for("main.autopartes"))
