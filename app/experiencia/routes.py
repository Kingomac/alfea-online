from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user


bp_experiencia = Blueprint(
    'experiencia', __name__, url_prefix='/experiencia', template_folder='templates')


@bp_experiencia.route('/', methods=['GET'])
def gastar_experiencia():
    combat_stats = current_user.get_combate_stats()
    return render_template('gastar_experiencia.html', combat_stats=combat_stats)
