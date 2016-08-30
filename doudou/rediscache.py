# -*- coding:utf-8 -*-
#
# 使用Redis为application增加缓存支持
#


import cPickle

from redis import Redis
from StringIO import StringIO
from functools import wraps
from flask import request, current_app

# Cache Object

class Cache(object):
    """
    Cache控制类
    """

    def __init__(self, app=None, redis=None):
        self.cache = None

        if app is not None and redis is not None:
            self.init_app(app, redis)
        else:
            self.app = None


    def init_app(self, app, redis=None):
        """
        使用app初始化cache
        """

        if redis is None:
            app.config.setdefault('CACHE_REDIS_SERVER', 'localhost')
            app.config.setdefault('CACHE_REDIS_PORT', 6379)
            app.config.setdefault('CACHE_REDIS_DB', 0)

            redis = Redis(host=app.config['CACHE_REDIS_SERVER'],
                          port=app.config['CACHE_REDIS_PORT'],
                          db=app.config['CACHE_REDIS_DB'])

        self.app = app

        self._set_cache(redis)


    def _set_cache(self, redis):

        self.cache = redis

    def get(self, key):
        """
        返回对应key的value
        """
        value = self.cache.get(key)
        if value is None:
            return None
        return cPickle.load(StringIO(value))

    def set(self, key, value, timeout=None):
        """
        设置缓存值
        :param key: cache_prefix
        :param value: cache_value
        :param timeout: cache_timeout
        :return:
        """

        stringio = StringIO()

        cPickle.dump(value, stringio)
        stringio.seek(0)
        self.cache.set(key, stringio.read())
        if timeout:
            self.cache.expire(key, timeout)

    def update(self, key, value):
        """
        更新对应键的值
        :param key:
        :param value:
        :return:
        """
        self.cache.delete(key)
        self.set(key, value)

    def delete(self, key):
        """
        清除对应key的缓存值
        :param key:
        :return:
        """
        self.cache.delete(key)


    def deletes(self, keys=[], pattern=None):
        """
        批量删除缓存对象
        :param keys:
        :param pattern:
        :return:
        """
        if pattern:
            keys = self.keys(pattern)
        for key in keys:
            self.cache.delete(key)

    def keys(self, pattern):
        """
        返回匹配的key集和
        :param pattern:
        :return:
        """
        return self.cache.keys(pattern)

    def cached(self, timeout=None, key_prefix='view/%s', unless=None):
        """
        缓存装饰器, 默认的缓存key=view/request.path, 你可以使用这个装饰器
        通过改变key_prefix,来取代默认的request.path
        例如:
        @cache.cached(timeout=50)
        def big_foo():
            return big_bar_calc()

        @cache_cached(key_prefix='cacheList')
        def get_cacheList():
            :return [random.randrange(0, 1) for i in range(50000)]
        :param timeout:
        :param key_prefix:
        :param unless:
        :return:
        """

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # : Bypass the cache entirely.
                if callable(unless) and unless() is True:
                    return f(*args, **kwargs)

                if '%s' in key_prefix:
                    cache_key = key_prefix % request.path
                else:
                    cache_key = key_prefix

                rv = self.get(cache_key)
                if rv is None:
                    rv = f(*args, **kwargs)
                    self.set(cache_key, rv, timeout=timeout)
                return rv

            return decorated_function

        return decorator