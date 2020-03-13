from flask import Flask
from flask_login import LoginManager, login_required
from nav import routes, auth

login_manager = LoginManager()


def make_app():
    app = Flask(__name__)
    app.debug = True
    app.port = 5000
    app.secret_key = 'Security!'
    app.config['BUNDLE_ERRORS'] = True

    auth.init_app(login_manager, app)

    routes.init_app(app)

    return app