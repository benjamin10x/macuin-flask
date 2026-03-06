from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import AutoparteForm
from .services import get_all_autopartes, get_autoparte_by_id, create_autoparte, update_autoparte, delete_autoparte

main = Blueprint("main", __name__)

@main.route("/")
def index():
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