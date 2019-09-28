def create_module(app):
    from .controllers import bp
    app.register_blueprint(bp)