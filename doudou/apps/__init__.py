# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 前台入口文件

from flask import Blueprint

app = Blueprint('apps', __name__, template_folder='./templates', static_folder='./static')

from . import views