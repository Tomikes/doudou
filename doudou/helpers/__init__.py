# -*- coding:utf-8 -*-
"""
helper 函数
"""

import os
import re
import hmac

from flask import render_template

from doudou import models
from doudou import cache

from base64 import b64encode
from hashlib import sha512


#重构模板渲染，简单支持定义theme
def render_theme_template(theme, template, **context):
    return render_template(''.join(os.path.join(theme, template)), **context)


#生成分类缓存
def get_sorts():
    result = cache.get("sorts")
    if result is None:
        sorts = models.Sort.query.filter_by(pid=0).all()
        result = []
        for sort in sorts:
            result.append(models.Sort.sort_children(sort))
        cache.set("sorts", result)
    return result


#更新分类缓存
def update_sorts():
    cache.delete("sorts")
    sorts = models.Sort.query.filter_by(pid=0).all()
    result = []
    for sort in sorts:
        result.append(models.Sort.sort_children(sort))
    cache.set("sorts", result)


#生成链接缓存
def get_links():
    result = cache.get("links")
    if result is None:
        result = models.Link.query.all()
        cache.set("links", result)
    return result


#更新链接缓存
def update_links():
    cache.update("links", models.Link.query.all())


#生成用户列表缓存
def get_users():
    result = cache.get("users")
    if result is None:
        result = models.User.query.all()
        cache.set("users", result)
    return result


#更新用户列表缓存
def update_users():
    cache.update("users", models.User.query.all())


# 参数检查
def _id_match(id):
    regex = re.compile(r'[0-9]')
    match = regex.match(id)
    if not match:
        return False
    else:
        return True


# 生成SHA512 HMAC
def generate_sha512_hmac(password_salt, password):
    return b64encode(hmac.new(password_salt, password.encode('utf-8'), sha512).digest())



# 密码加密
def hash_password(password_salt, password):
    hashed_password = generate_sha512_hmac(password_salt, password)
    return hashed_password


#验证密码是否正确
def verify_password(password_salt, form_password, user_password):
    password = generate_sha512_hmac(password_salt, form_password)
    return password == user_password