from flask import Flask
from app import bp_usuarios
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'magicwinx'

app.register_blueprint(bp_usuarios)

if __name__ == '__main__':
    app.run(debug=True)
