from flask import Blueprint, render_template, send_file, url_for, send_from_directory

bp_lore = Blueprint('lore', __name__, url_prefix='/lore',
                    template_folder='templates', static_folder='static')


@bp_lore.route('/moneda')
def moneda():
    return render_template('moneda.html')
