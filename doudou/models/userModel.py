# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# User Model

from doudou.extensions import db

# 表前缀
prefix = 'doudou'


ROLE_ADMIN = '0'
ROLE_USERS = '1'

class User(db.Model):

    __tablename__ = "%s_user" % prefix

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(32), nullable=False, default='', index=True, unique=True)
    password = db.Column(db.VARCHAR(100), nullable=False, default='')
    nickname = db.Column(db.VARCHAR(20), nullable=False, default='')
    role = db.Column(db.Enum(ROLE_USERS, ROLE_ADMIN), nullable=False, default=ROLE_USERS)
    ischeck = db.Column(db.Enum('n', 'y'), nullable=False, default='y')
    photo = db.Column(db.VARCHAR(255), nullable=False, default='')
    email = db.Column(db.VARCHAR(60), nullable=False, default='')
    description = db.Column(db.VARCHAR(255), nullable=False, default='')

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.ischeck == 'y':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.uid)

    @staticmethod
    def make_username_unique(username):
        if User.query.filter_by(username=username).first() == None:
            return username
        else:
            return False

    def __repr__(self):
        return '<User %r>' % (self.nickname)