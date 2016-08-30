# -*- coding:utf-8 -*-
"""
    helpers.__init__.py

    :add extensions to applications
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from doudou.rediscache import Cache
from redis import Redis

__all__ = ["db", "cache", "rds", "lgm"]

db = SQLAlchemy()
cache = Cache()
rds = Redis()
lgm = LoginManager()