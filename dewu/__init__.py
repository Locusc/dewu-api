import os

from flask import Flask

from dewu.blueprints.api.du_api_blueprint import du_api_bp
from dewu.extensions import db, moment, redis_store
from dewu.setting import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    app.register_blueprint(du_api_bp, url_prefix='/api')


def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    redis_store.init_app(app)
