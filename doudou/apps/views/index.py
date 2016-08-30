# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 首页入口文件

import StringIO

import os

from flask import session, make_response, send_file

from doudou.extensions import db
from doudou.apps import app
from doudou.createVcode import create_valicode


@app.route('/')
def index():
    return 'Hello,World'

@app.route('/crossdomain.xml')
def cross_domain():
    filename = os.path.join(app.root_path, 'static/crossdomain.xml')
    return send_file(filename)

@app.route('/favicon.ico')
def get_favicon():
    filename = os.path.join(app.root_path, 'static/favicon.ico')
    return send_file(filename)

@app.route('/create_authcode')
def create_auth_code():
    img, strs = create_valicode(bg_color=(105, 105, 105), length=6, draw_points=False)
    buf = StringIO.StringIO()
    img.save(buf, 'JPEG', quality=70)
    session['auth_code'] = strs
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'

    return response


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
