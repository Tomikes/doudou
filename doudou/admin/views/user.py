# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 用户

import hashlib

from flask import request, flash, redirect, url_for, \
    abort, current_app, g

from werkzeug.utils import secure_filename

from base64 import b64encode

from flask.ext.login import login_required
from MySQLdb import MySQLError

from doudou.models import User
from doudou.admin import admin, theme
from doudou.forms import UserForm, EditUserForm, ProfileForm
from doudou.helpers import render_theme_template
from doudou.helpers import get_users, update_users
from doudou.helpers import _id_match, hash_password
from doudou.extensions import db

import os, time


@admin.route('/user', methods=["GET", "POST"])
@login_required
def user():
    if request.args.get('action') == 'add':

        if g.user.role != '0':
            flash(u'您不是管理员,没有权限添加用户', 'error')
            return redirect(url_for('admin.user'))

        form = UserForm()

        if request.method == "POST" and form.validate_on_submit():
            password = hash_password(current_app.config['SECRET_KEY'], form.password.data)
            role = request.form.get('role')
            ischeck = request.form.get('ischeck')

            if User.make_username_unique(form.username.data):
                username = form.username.data

                us = User(username=username, password=password, role=role, ischeck=ischeck)

                try:
                    db.session.add(us)
                    db.session.commit()
                    update_users()
                    flash(u'添加用户成功', 'success')
                except MySQLError, e:
                    flash(u'添加用户失败,失败原因: %s' % e, 'error')

                return redirect(url_for('admin.user'))

            else:
                form.username.errors.append(u'用户名已经存在')

        return render_theme_template(theme, 'addUser.html', form=form)

    if request.args.get('action') == 'update':

        uid = request.args.get('uid', None)
        if uid:
            if not _id_match(uid):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.user'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.user'))

        # 对uid进行格式转换
        # uid = int(uid)

        # 判断当前登陆用户是否为管理员
        if g.user.role != '0':
            flash(u'您不是管理员,没有权限修改用户的信息.', 'error')
            return redirect(url_for('admin.user'))

        # 构建表单
        form = EditUserForm()

        us = User.query.filter_by(uid=uid).first()

        if request.method == "POST" and form.validate_on_submit():
            us.password = hash_password(current_app.config['SECRET_KEY'], form.password.data) \
                if form.password.data and hash_password(current_app.config['SECRET_KEY'], form.password.data) != \
                                          us.password else us.password
            us.role = request.form.get('role') if request.form.get('role') != us.role else us.role
            us.ischeck = request.form.get('ischeck') if request.form.get('ischeck') != \
                                                        us.ischeck else us.ischeck

            if form.username.data != us.username:
                if User.make_username_unique(form.username.data):
                    us.username = form.username
                    try:
                        db.session.add(us)
                        db.session.commit()
                        update_users()
                        flash(u'修改用户信息成功', 'success')
                    except MySQLError, e:
                        flash(u'修改信息失败,失败原因: %s' % e, 'error')

                    return redirect(url_for('admin.user'))
                else:
                    form.username.errors.append(u'用户名已经存在了')
            else:
                us.username = us.username

                try:
                    db.session.add(us)
                    db.session.commit()
                    update_users()
                    flash(u'修改用户信息成功', 'success')
                except MySQLError, e:
                    flash(u'修改信息失败,失败原因: %s' % e, 'error')

                return redirect(url_for('admin.user'))

        return render_theme_template(theme, 'editUser.html', form=form, us=us)

    if request.args.get('action') == 'del':

        if g.user.role != '0':
            flash(u'您不是管理员,没有权限删除用户', 'error')
            return redirect(url_for('admin.user'))

        uid = request.args.get('uid', None)
        if uid:
            if not _id_match(uid):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.user'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.user'))

        us = User.query.filter_by(uid=uid).first()
        if us:
            try:
                db.session.delete(us)
                db.session.commit()
                update_users()
                flash(u'删除用户成功', 'success')
            except MySQLError, e:
                flash(u'删除用户失败,失败原因: %s' % e, 'error')
        else:
            flash(u'不存在此用户', 'error')

        return redirect(url_for('admin.user'))

    users = get_users()
    return render_theme_template(theme, 'user.html', users=users)


@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if request.args.get('action') == 'update':
        if request.method == 'GET':
            abort(405)
        if request.method == "POST" and form.validate_on_submit():
            g.user.password = hash_password(current_app.config['SECRET_KEY'], form.password.data) \
                if form.password.data and hash_password(current_app.config['SECRET_KEY'], form.password.data) != \
                                          g.user.password else g.user.password
            g.user.nickname = form.nickname.data \
                if form.nickname.data and form.nickname.data != \
                                          g.user.nickname else g.user.nickname
            g.user.email = form.email.data if form.email.data and form.email.data != g.user.email else g.user.email
            g.user.description = form.description.data

            if form.username.data != g.user.username:
                if User.make_username_unique(form.username.data):
                    g.user.username = form.username
                    try:
                        db.session.add(g.user)
                        db.session.commit()
                        update_users()
                        flash(u'修改个人信息成功', 'success')
                    except MySQLError, e:
                        flash(u'修改个人失败,失败原因: %s' % e, 'error')

                    return redirect(url_for('admin.profile'))
                else:
                    form.username.errors.append(u'用户名已经存在了')
            else:
                g.user.username = g.user.username

                try:
                    db.session.add(g.user)
                    db.session.commit()
                    update_users()
                    flash(u'修改个人信息成功', 'success')
                except MySQLError, e:
                    flash(u'修改个人失败,失败原因: %s' % e, 'error')

                return redirect(url_for('admin.profile'))

    # 初始化个人描述的值
    form.description.data = g.user.description

    # 初始化人物头像
    avatar_path = os.path.join('avatar', g.user.photo)
    return render_theme_template(theme, 'profile.html', form=form, avatar_path=avatar_path)


@admin.route('/avatar_upload', methods=["POST"])
@login_required
def avatar_upload():
    avatar_img = request.files.get('avatar', None)

    # 头像保存目录
    save_path = os.path.join(admin.root_path, 'static/avatar')

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 重构文件名
    filename = b64encode(secure_filename(avatar_img.filename) + str(int(time.time())) + g.user.username) + '.jpg'
    #保存文件
    try:
        avatar_img.save(os.path.join(save_path, filename))
    except Exception, e:
        return u'error'

    #删除用户旧的头像
    if g.user.photo:
        old_avatar = os.path.join(save_path, g.user.photo)
        if os.path.exists(old_avatar) and os.path.isfile(old_avatar):
            os.remove(old_avatar)

    #更新数据库
    g.user.photo = filename

    try:
        db.session.add(g.user)
        db.session.commit()
        return 'success'
    except MySQLError, e:
        return u'error'
