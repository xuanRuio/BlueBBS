# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# # forms表单信息
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo


class BaseForm(Form):
    errors = {
        'message': '表单信息填写错误'
    }

    def get_err(self):
        return self.errors["message"]


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(3, 15, message='请输入正确长度的密码')])
    remember = IntegerField()


# 修改密码页面中的form表单信息
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(3, 15, message="密码长度有误")])
    newpwd = StringField(validators=[Length(3, 15, message="密码长度有误")])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="两次输入密码不一致")])
