# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# Blog Model

from doudou.extensions import db

# 表前缀
prefix = 'doudou'


class Blog(db.Model):
    __tablename__ = '%s_blog' % prefix

    gid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(255), nullable=False, default='')
    date = db.Column(db.BigInteger, nullable=False, default='')
    content = db.Column(db.Text, nullable=False, default='')
    excerpt = db.Column(db.Text, nullable=False, default='')
    tags = db.Column(db.Text, nullable=False, default='')
    author = db.Column(db.Integer, nullable=False, default='1')
    sortid = db.Column(db.Integer, nullable=False, default='-1')
    views = db.Column(db.Integer, nullable=False, default='0')
    comnum = db.Column(db.Integer, nullable=False, default='0')
    top = db.Column(db.Enum('n', 'y'), nullable=False, default='n')
    sorttop = db.Column(db.Enum('n', 'y'), nullable=False, default='n')
    hide = db.Column(db.Enum('n', 'y'), nullable=False, default='n')


    def __repr__(self):
        return '<Blog %r>' % self.title