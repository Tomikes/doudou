# coding:utf-8
"""
    __init__.py

    :init Application
"""

from flask import Flask
from datetime import timedelta
from .extensions import db, rds
from .extensions import lgm, cache
from . import apps
from . import admin
from . import kindeditor
from . import sessions


DEFAULT_BLUEPRINTS = (
    (apps.app, ""),
    (admin.admin, "/doudou/admin"),
    (kindeditor.kindedit, '/attached')
)


def create_app(config=None, blueprints=None):
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(__name__)

    app.config.from_pyfile(config)

    add_extensions(app)

    configure_context_processors(app)

    configure_blueprints(app, blueprints)

    configure_session_lifetime(app)

    return app


def add_extensions(app):
    db.init_app(app)

    cache.init_app(app, rds)

    lgm.init_app(app)
    lgm.login_view = 'admin.login'

    if app.config.has_key('REDIS'):
        host = app.config['REDIS']['host']
        port = app.config['REDIS']['port']
        rdb = app.config['REDIS']['rdb']
        pwd = app.config['REDIS']['pwd']

        rds.__init__(host, port, rdb, pwd)

    app.session_interface = sessions.RedisSessionInterface(rds)


def configure_context_processors(app):
    @app.context_processor
    def config():
        return dict(config=app.config)


def configure_blueprints(app, blueprints):
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_session_lifetime(app):
    if app.config.has_key('SESSION_LIFETIME'):
        app.permanent_session_lifetime = timedelta(seconds=app.config['SESSION_LIFETIME'])
