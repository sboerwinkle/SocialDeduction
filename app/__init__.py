from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

static_folder = "../client/build"
template_folder = "../client/build"

def create_app(debug=False):
    """Create an application."""
    # app = Flask(__name__, static_url_path='',
    #               static_folder=static_folder,
    #               template_folder=template_folder)

    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'TODO'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
