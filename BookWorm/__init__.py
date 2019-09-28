from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    """
    Flask application factory

    :param config: Path to python config file
    """
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup database
    # TODO: Migration
    db.init_app(app)

    # Import modules
    from .main import create_module as create_main_module
    create_main_module(app)

    from .auth import create_module as create_auth_module
    create_auth_module(app)

    from .dashboard import create_module as create_dashboard_module
    create_dashboard_module(app)

    return app
