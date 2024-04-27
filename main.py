from flask import Flask, send_from_directory
from app import bp_usuarios, bp_chat, registar_sockets, bp_ui, bp_combate, registrar_sockets_lobby_combate
import redis
from flask_login import LoginManager
from app.usuarios.model import Usuario
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'magicwinx'
socketio = SocketIO(app)

login_manager = LoginManager(app)
login_manager.login_view = 'usuarios.index'

app.register_blueprint(bp_usuarios)
app.register_blueprint(bp_chat)
app.register_blueprint(bp_ui)
app.register_blueprint(bp_combate)

registar_sockets(socketio)
registrar_sockets_lobby_combate(socketio)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return 'Unauthorized'


@login_manager.user_loader
def load_user(nombre):
    return Usuario.find_by_name(nombre)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    socketio.run(app, debug=True)
