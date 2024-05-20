from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from db import redis_db
from .model import Mensaje
import json
import flask_login
from flask_login import current_user
from .service import get_lista_amigos

bp_chat = Blueprint('chat', __name__, url_prefix='/chat',
                    template_folder='templates')


@bp_chat.route('/')
@flask_login.login_required
def chat():
    amigos = get_lista_amigos(current_user.nombre)
    return render_template('chat.html', amigos=amigos)
