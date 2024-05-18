from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, send_file
from os.path import isfile

bp_perfil = Blueprint('perfil', __name__, url_prefix='/perfil',
                      template_folder='templates', static_folder='static')


@bp_perfil.route('/<nombre>/foto')
def foto_perfil(nombre):
    if isfile(f'static/img/fotos_perfil/{nombre}.webp'):
        return send_from_directory('static/img/fotos_perfil', f'{nombre}.webp')
    return send_file('static/img/fotos_perfil/default.webp')
