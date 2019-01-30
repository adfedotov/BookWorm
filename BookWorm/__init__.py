from flask import Flask, render_template

def create_app(config):

    app = Flask(__name__)

    app.config.from_object(config)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
