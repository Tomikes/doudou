# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# Link Model

from doudou.extensions import db

# 表前缀
prefix = 'doudou'


class Link(db.Model):
    __tablename__ = '%s_link' % prefix

    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.VARCHAR(30), nullable=False, default='')
    siteurl = db.Column(db.VARCHAR(75), nullable=False, default='')
    description = db.Column(db.VARCHAR(255), nullable=False, default='')
    hide = db.Column(db.Enum('n', 'y'), nullable=False, default='n')
    taxis = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Link %r>' % (self.sitename)