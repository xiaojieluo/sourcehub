def init_routes(app):
    # from sourcehub.controller import index_bp, tag_bp, user_bp, link_bp, website_bp
    # from sourcehub.controller import index_bp
    from sourcehub.controller.IndexController import index as index_bp
    from sourcehub.controller.WebsiteController import website as website
    from sourcehub.controller.UserController import user
    from sourcehub.controller.TagController import tag
    app.register_blueprint(index_bp)
    app.register_blueprint(tag)
    app.register_blueprint(user)
    # app.register_blueprint(link_bp)
    app.register_blueprint(website)


def init_api_routes(app):
    # from sourcehub.api import index_api, link_api, user_api, site_api, tag_api
    from sourcehub.api import index_api
    from sourcehub.api import site_api
    from sourcehub.api import app_api
    app.register_blueprint(index_api, url_prefix='/')
    app.register_blueprint(app_api, url_prefix='/api/app/')
    # app.register_blueprint(link_api)
    # app.register_blueprint(user_api)
    app.register_blueprint(site_api, url_prefix='/api/sites')
    # app.register_blueprint(tag_api)


def init_app(app):
    # init_routes(app)
    init_api_routes(app)
