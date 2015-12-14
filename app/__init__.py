from flask import Flask
from flask.ext.socketio import SocketIO
import os
socketio = SocketIO()
from models import db

def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://anthony:dx9Vzxq6fr@localhost/vpnp'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    db.init_app(app=app)
    socketio.init_app(app)
    return app

