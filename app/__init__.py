"""__init__.py."""

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db variable initialization
db = SQLAlchemy()

# local imports
from config import app_config
from app.endpoints import api_blueprint




def create_app(config_name):
    """Create app."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    app.register_blueprint(api_blueprint)
    return app
