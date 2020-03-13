def init_routes(app):
    from nav.controller import index_bp, tag_bp, user_bp, link_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(link_bp)


def init_api_routes(app):
    from nav.api import index_api, link_api
    app.register_blueprint(index_api)
    app.register_blueprint(link_api)


def init_app(app):
    init_routes(app)
    init_api_routes(app)