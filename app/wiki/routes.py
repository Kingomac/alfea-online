from flask import Blueprint, render_template, send_file, url_for, send_from_directory

bp_wiki = Blueprint('wiki', __name__, url_prefix='/wiki',
                    template_folder='templates', static_folder='static')


@bp_wiki.route('/moneda')
def moneda():
    return render_template('moneda.html')


@bp_wiki.route('/experiencia')
def experiencia():
    return render_template('experiencia.html')


@bp_wiki.route('/movil')
def movil():
    return render_template('movil.html')


@bp_wiki.route('/estadisticas-combate')
def estadisticas_combate():
    return render_template('estadisticas_combate.html')


@bp_wiki.route('/flechas-magicas')
def flechas_magicas():
    return render_template('flechas_magicas.html')


@bp_wiki.route('/salas-chat')
def salas_chat():
    return render_template('salas_chat.html')


@bp_wiki.route('/')
def index():
    return render_template('index.html')
