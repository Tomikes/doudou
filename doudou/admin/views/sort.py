# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 分类

from flask import request, flash, redirect, url_for, \
    abort

from flask.ext.login import login_required
from MySQLdb import MySQLError

from doudou.models import Sort
from doudou.admin import admin, theme
from doudou.forms import SortForm
from doudou.helpers import render_theme_template
from doudou.helpers import get_sorts, update_sorts
from doudou.helpers import _id_match
from doudou.extensions import db


@admin.route('/sort', methods=["GET", "POST"])
@login_required
def sort():
    p_sorts = Sort.query.filter_by(pid=0).all()
    if request.args.get('action') == 'add':
        form = SortForm()
        if request.method == "POST" and form.validate_on_submit():
            taxis = form.taxis.data
            sortname = form.sortname.data
            alias = form.alias.data
            pid = request.form.get('pid')
            description = form.description.data

            if Sort.make_alias_uniqu(alias):
                sort = Sort(taxis=taxis, sortname=sortname, alias=alias, \
                            pid=pid, description=description)

                try:
                    db.session.add(sort)
                    db.session.commit()
                    update_sorts()  # 更新分类缓存
                    flash(u'添加分类成功', 'success')
                except MySQLError, e:
                    flash(u'添加分类失败,失败原因: %s' % e, 'error')
                finally:
                    return redirect(url_for('admin.sort'))
            else:
                form.alias.errors.append(u'别名不能重复')

        return render_theme_template(theme, 'addSort.html', \
                                     form=form, p_sorts=p_sorts)

    if request.args.get('action') == 'update':
        form = SortForm()
        sid = request.args.get('sid', None)
        if sid:
            if not _id_match(sid):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.sort'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.sort'))

        sort = Sort.sort_children(Sort.query.filter_by(sid=sid).first())

        if request.method == "POST" and form.validate_on_submit():
            sort.taxis = form.taxis.data if form.taxis.data != sort.taxis else sort.taxis
            sort.sortname = form.sortname.data if form.sortname.data != sort.sortname else sort.sortname
            sort.pid = request.form.get('pid') if request.form.get('pid') and request.form.get(
                'pid') != sort.pid else sort.pid
            sort.description = form.description.data if form.description.data != sort.description \
                else sort.description

            # 判断别名重复
            if sort.alias != form.alias.data:
                if Sort.make_alias_uniqu(form.alias.data):
                    sort.alias = form.alias.data
                    # 提交数据
                    try:
                        db.session.add(sort)
                        db.session.commit()
                        update_sorts()  # 更新缓存
                        flash(u'修改分类成功', 'success')
                    except MySQLError, e:
                        flash(u'修改分类失败,失败原因: %s' % e, 'error')
                    return redirect(url_for('admin.sort'))
                else:
                    form.alias.errors.append(u'别名不能重复')
            else:
                sort.alias = sort.alias
                try:
                    db.session.add(sort)
                    db.session.commit()
                    update_sorts()
                    flash(u'修改分类成功', 'success')
                except MySQLError, e:
                    flash(u'修改分类失败,失败原因: %s' % e, 'error')
                return redirect(url_for('admin.sort'))

        # 初始化分类描述的值
        form.description.data = sort.description

        return render_theme_template(theme, 'editSort.html', form=form, \
                                     sort=sort, p_sorts=p_sorts)

    if request.args.get('action') == 'del':
        if request.method == 'POST':
            abort(405)

        sid = request.args.get('sid', None)
        if sid:
            if not _id_match(sid):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.sort'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.sort'))

        sort = Sort.query.filter_by(sid=sid).first()

        if sort:
            sort = Sort.sort_children(sort)
            if len(sort.childrens) == 0:
                try:
                    db.session.delete(sort)
                    db.session.commit()
                    update_sorts()
                    flash(u'删除分类成功', 'success')
                except MySQLError, e:
                    flash(u'删除分类失败,失败原因: %s' % e, 'error')
            else:
                flash(u'分类存在子分类，请先删除子分类', 'error')
        else:
            flash(u'不存在此分类', 'error')
        return redirect(url_for('admin.sort'))

    sorts = get_sorts()
    form = SortForm()
    return render_theme_template(theme, 'sort.html', sorts=sorts, form=form, p_sorts=p_sorts)