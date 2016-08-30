# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# 友链

from flask import request, flash, redirect, url_for, \
    abort

from flask.ext.login import login_required
from MySQLdb import MySQLError

from doudou.models import Link
from doudou.admin import admin, theme
from doudou.forms import LinkForm
from doudou.helpers import render_theme_template
from doudou.helpers import get_links, update_links
from doudou.helpers import _id_match
from doudou.extensions import db


@admin.route('/link', methods=["GET", "POST"])
@login_required
def link():
    if request.args.get('action') == 'add':
        form = LinkForm()
        if request.method == "POST" and form.validate_on_submit():
            taxis = form.taxis.data
            sitename = form.sitename.data
            siteurl = form.siteurl.data
            description = form.description.data
            hide = request.form.get('hide')

            lnk = Link(taxis=taxis, sitename=sitename, siteurl=siteurl, hide=hide, \
                       description=description)

            try:
                db.session.add(lnk)
                db.session.commit()
                update_links()
                flash(u'增加友链成功', 'success')
            except MySQLError, e:
                flash(u'增加友链失败,失败原因: %s' % e, 'error')
            finally:
                return redirect(url_for('admin.link'))
        return render_theme_template(theme, 'addLink.html', form=form)

    if request.args.get('action') == 'update':
        form = LinkForm()
        id = request.args.get('id', None)
        if id:
            if not _id_match(id):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.link'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.link'))

        lnk = Link.query.filter_by(id=id).first()

        if request.method == "POST" and form.validate_on_submit():
            lnk.taxis = form.taxis.data if form.taxis.data != lnk.taxis else lnk.taxis
            lnk.sitename = form.sitename.data if form.sitename.data != lnk.sitename else lnk.sitename
            lnk.siteurl = form.siteurl.data if form.siteurl.data != lnk.siteurl else lnk.siteurl
            lnk.description = form.description.data if form.description.data else lnk.description
            lnk.hide = request.form.get('hide') if request.form.get('hide') and request.form.get(
                'hide') != lnk.hide else lnk.hide

            try:
                db.session.add(lnk)
                db.session.commit()
                update_links()
                flash(u'修改链接信息成功', 'success')
            except MySQLError, e:
                flash(u'修改失败,失败原因: %s' % e, 'error')

            return redirect(url_for('admin.link'))

        # 给描述默认值
        form.description.data = lnk.description

        return render_theme_template(theme, 'editLink.html', form=form, lnk=lnk)

    if request.args.get('action') == 'del':
        id = request.args.get('id', None)
        if id:
            if not _id_match(id):
                flash(u'参数错误', 'error')
                return redirect(url_for('admin.link'))
        else:
            flash(u'参数错误', 'error')
            return redirect(url_for('admin.link'))

        lnk = Link.query.filter_by(id=id).first()

        if lnk:
            try:
                db.session.delete(lnk)
                db.session.commit()
                update_links()
                flash(u'链接删除成功', 'success')
            except MySQLError, e:
                flash(u'链接删除失败, 失败原因: %s' % e, 'error')
        else:
            flash(u'不存在此链接', 'error')

        return redirect(url_for('admin.link'))

    links = get_links()
    return render_theme_template(theme, 'link.html', links=links)