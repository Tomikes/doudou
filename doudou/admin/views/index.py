# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# doudou 后端首页

from flask import make_response, request
from flask import url_for, g, redirect, current_app

from flask.ext.login import current_user, login_required, \
    login_user, logout_user
from sqlalchemy import or_

from doudou.admin import admin, theme
from doudou.extensions import lgm
from doudou.models import User
from doudou.forms import LoginForm
from doudou.helpers import render_theme_template
from doudou.helpers import verify_password
from doudou.extensions import cache


@admin.before_request
def before_request():
    g.user = current_user


@lgm.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


@admin.route('/')
@login_required
def index():
    return render_theme_template(theme, 'index.html')


@admin.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter(or_(User.username == username, User.email == username)).first()

        if user and user.is_active():
            if verify_password(current_app.config['SECRET_KEY'], password, user.password):
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get('next') or url_for('admin.index'))
            else:
                form.password.errors.append(u'您输入的密码不正确')
        else:
            form.username.errors.append(u'用户名或邮箱不正确')
    return render_theme_template(theme, 'login.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
