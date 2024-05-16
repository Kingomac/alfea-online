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


@bp_wiki.route('/')
def index():
    return render_template('index.html')
