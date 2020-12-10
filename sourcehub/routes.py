def init_api_routes(app):
    """api routes

    Args:
        app ([type]): [description]
    """
    from sourcehub.api import index_api, site_api, app_api, user_api, link_api, tag_api

    app.register_blueprint(index_api, url_prefix='/api/')
    app.register_blueprint(app_api, url_prefix='/api/app/')
    app.register_blueprint(user_api, url_prefix='/api/users/')
    app.register_blueprint(site_api, url_prefix='/api/sites/')
    app.register_blueprint(link_api, url_prefix='/api/links/')
    app.register_blueprint(tag_api, url_prefix='/api/tags/')


def init_app(app):
    init_api_routes(app)
