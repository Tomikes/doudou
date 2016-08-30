# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 管理后台入口文件

from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='./templates', static_folder='./static')

theme = 'default'

from . import views