# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# Sort Model

from doudou.extensions import db

# 表前缀
prefix = 'doudou'


class Sort(db.Model):
    __tablename__ = '%s_sort' % prefix

    sid = db.Column(db.Integer(), primary_key=True)
    sortname = db.Column(db.VARCHAR(255), nullable=False, default='')
    alias = db.Column(db.VARCHAR(200), nullable=False, default='')
    taxis = db.Column(db.Integer(), nullable=False, default=0)
    description = db.Column(db.VARCHAR(1024), nullable=False, default='')
    pid = db.Column(db.Integer(), nullable=False, default=0)


    @staticmethod
    def make_alias_uniqu(alias):
        if Sort.query.filter_by(alias=alias).first() == None:
            return alias
        else:
            return False

    @staticmethod
    def sort_children(sort):
        childs = Sort.query.filter_by(pid=sort.sid).all()
        sort.childrens = childs
        return sort

    def __repr__(self):
        return '<Sort %r>' % (self.sortname)