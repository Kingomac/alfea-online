from flask import Blueprint, render_template, send_file, url_for, send_from_directory

bp_wiki = Blueprint('wiki', __name__, url_prefix='/wiki',
                    template_folder='templates', static_folder='static')


@bp_wiki.route('/moneda')
def moneda():
    return render_template('moneda.html')
