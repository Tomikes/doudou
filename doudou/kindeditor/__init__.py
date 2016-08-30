# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# kindeditor配置文件

from flask import Blueprint

kindedit = Blueprint('kindedit', __name__, static_folder='./uploadFile')

from . import views