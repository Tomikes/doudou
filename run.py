# -*- coding:utf-8 -*-
"""
    doudou_master.py

    :run application on debug
"""

from doudou import create_app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = create_app('config.cfg')

server = HTTPServer(WSGIContainer(app))

if __name__ == '__main__':
    server.listen(8047)
    IOLoop.instance().start()