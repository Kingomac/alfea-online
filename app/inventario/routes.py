from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.ataque.service import get_ataques_equipados_usuario, get_ataques_usuario
from flask_login import current_user
from .service import equipar_ataque, desequipar_ataque
import json

bp_inventario = Blueprint('inventario', __name__,
                          url_prefix='/inventario', template_folder='templates', static_folder='static')


@bp_inventario.route('/')
def index():
    ataques_equipados = get_ataques_equipados_usuario(current_user.nombre)
    ids_ataques_equipados = [x.id for x in ataques_equipados]
    ataques_no_equipados = [x for x in get_ataques_usuario(
        current_user.nombre) if x.id not in ids_ataques_equipados]
    return render_template('inventario.html', ataques_equipados=ataques_equipados, ataques_no_equipados=ataques_no_equipados)


@bp_inventario.route('/ataque', methods=['POST'])  # Equipar
def equipar():
    if request.headers['Content-Type'] != 'application/json':
        return "Content-Type must be application/json", 400
    ataque_id = request.json['ataque_id']
    return json.dumps(equipar_ataque(current_user, ataque_id))


@bp_inventario.route('/ataque', methods=['DELETE'])  # Desequipar
def desequipar():
    if request.headers['Content-Type'] != 'application/json':
        return "Content-Type must be application/json", 400
    ataque_id = request.json['ataque_id']
    return json.dumps(desequipar_ataque(current_user, ataque_id))
