from flask import Flask

def create_app(config):

    app = Flask(__name__)

    app.config.from_object(config)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app
