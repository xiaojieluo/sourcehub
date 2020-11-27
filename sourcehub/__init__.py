from flask import Flask
from flask_login import LoginManager, login_required
from flask_cors import *
from sourcehub import routes
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
api_url = 'http://localhost:5000'

db = SQLAlchemy()


def make_app():
    app = Flask(__name__)
    app.port = 5000
    app.secret_key = 'Security!'
    app.config['BUNDLE_ERRORS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sourcehub:sourcehub@localhost/sourcehub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    db.init_app(app)

    login_manager.init_app(app)

    # auth.init_app(login_manager, app)

    routes.init_app(app)

    return app