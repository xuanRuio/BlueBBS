# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# # forms表单信息
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, EqualTo, Regexp, ValidationError

from utils import redis_captcha


class BaseForm(Form):
    errors = {
        'message': '表单信息填写错误'
    }
    def get_error(self):
        return self.errors["message"]


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确格式的手机号")])
    sms_captcha = StringField(validators=[Regexp(r'\w{6}', message="请输入正确格式的验证码")])  # \w包含字母
    username = StringField(validators=[Length(min=3, max=15, message="请输入正确长度的用户名")])
    password1 = StringField(validators=[Regexp(r'[_a-zA-Z0-9]{3,20}', message="请输入正确格式的密码")])  # \u4e00-\u9fa5
    password2 = StringField(validators=[EqualTo('password1', message="两次输入密码不一致")])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message="请输入正确格式的验证码")])

    # 验证手机验证码字段
    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = self.sms_captcha.data  # 获得表单信息
        sms_captcha_redis = redis_captcha.redis_get(telephone)  # redis数据库中根据手机号调验证码，进行判定是否相同
        # 判断用户输入的验证码和redis中取出的验证码是否相同
        if not sms_captcha_redis or sms_captcha_redis != sms_captcha:
            print('自定义表单手机验证码验证失败')
            raise ValidationError(message="验证码输入错误")

    # 图形验证码字段验证
    def validate_graph_captcha(self, field):
        # 表单验证码  转小写
        graph_captcha = self.graph_captcha.data  # 表单信息收集
        graph_captcha = graph_captcha.lower()
        # 验证数据库验证码
        graph_captcha_redis = redis_captcha.redis_get(graph_captcha)  # redis中是将验证码的text当做key来保存的，调用也是一样
        # 判定图形验证码是否一致
        if not graph_captcha_redis or graph_captcha_redis != graph_captcha:
            print('自定义表单图片验证码验证失败')
            raise ValidationError(message="图形验证码输入错误")




class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确格式的手机号")])
    password = StringField(validators=[Regexp(r'[_a-zA-Z0-9]{3,20}', message="请输入正确格式的密码")])
    remember = IntegerField()









