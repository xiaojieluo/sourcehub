from flask_login import LoginManager, login_required


def init_app(login_manager, app):
    # login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login.html'
    login_manager.login_message = 'Unauthorized User'
    login_manager.login_message_category = "info"
