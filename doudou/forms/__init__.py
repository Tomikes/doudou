# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'


from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, \
    BooleanField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import Length, URL
from flask import session
import re

# 序号验证器
def taxis_helper(form, field):
    regex = re.compile(r'[0-9]')
    match = regex.match(field.data)
    if not match:
        raise ValidationError(u'序号只能为数字')


# 别名验证器
def alias_helper(form, field):
    regex = re.compile(r'[a-zA-Z]')
    if field.data:
        match = regex.match(field.data)
        if not match:
            raise ValidationError(u'别名只能使用字母')


# 用户名验证器
def username_helper(form, field):
    regex = re.compile(r'[a-zA-Z]')
    if field.data:
        match = regex.match(field.data)
        if not match:
            raise ValidationError(u'用户名只能使用字母')


# 邮箱验证器
def email_helper(form, field):
    regex = re.compile(r'^.+@([^.@][^@]+)$')
    if field.data != '':
        match = regex.match(field.data)
        if not match:
            raise ValidationError(u'邮箱地址错误')


# 验证码验证器
def authCode_helper(form, field):
    authCode = field.data
    if authCode != session['auth_code']:
        raise ValidationError(u'验证码错误')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message=u'用户名不能为空'), username_helper])
    password = PasswordField('password', validators=[DataRequired(message=u'密码不能为空')])
    authcode = StringField('authcode', validators=[DataRequired(message=u'验证码不能为空'), authCode_helper])
    remember_me = BooleanField('remember', default=False)


class UserForm(Form):
    username = StringField('username', validators=[DataRequired(message=u'用户名不能为空'), username_helper])
    password = PasswordField('password', validators=[DataRequired(message=u'密码不能为空')])


class EditUserForm(Form):
    username = StringField('username', validators=[DataRequired(message=u'用户名不能为空'), username_helper])
    password = PasswordField('password')


class SortForm(Form):
    taxis = StringField('taxis', validators=[DataRequired(message=u'序号不能为空'), taxis_helper])
    sortname = StringField('sortname', validators=[DataRequired(message=u'分类名称不能为空')])
    alias = StringField('alias', validators=[DataRequired(message=u'别名不能为空'), alias_helper])
    description = TextAreaField('descripttion', validators=[Length(max=200, message=u'描述不能超过200字')])


class LinkForm(Form):
    taxis = StringField('taxis', validators=[DataRequired(message=u'序号不能为空'), taxis_helper])
    sitename = StringField('sitename', validators=[DataRequired(message=u'友链名称不能为空')])
    siteurl = StringField('siteurl', validators=[DataRequired(message=u'友链地址不能为空'), URL(message=u'请输入正确的链接格式')])
    description = TextAreaField('description', validators=[Length(max=200, message=u'描述不能超过200字')])


class ProfileForm(Form):
    username = StringField('username', validators=[username_helper])
    password = PasswordField('password')
    nickname = StringField('nickname')
    email = StringField('email', validators=[email_helper])
    description = TextAreaField('description', validators=[Length(max=200, message=u'描述不能超过200字')])


# 添加blog Form
class AddForm(Form):
    title = StringField('title', validators=[DataRequired(message=u'blog标题不能为空')])
    content = TextAreaField('content')
    excerpt = TextAreaField('excerpt')
