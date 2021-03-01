# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""

# 导入手机验证码生成文件
from utils import restful, redis_captcha
from utils.captcha import Captcha
from utils.sms_ronglianyun.SendMessage import send_message
from utils.random_captcha import get_random_captcha
from flask import request
from . import common_bp
# 手机验证码生成文件
from .forms import SMSCaptchaForm
from random import randint


# 手机验证码生成文件，这部分是只要调用当前路由请求，就会发送短信验证码，
# 需要利用sign = md5(timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%")，在front_signup.js文件中调用
# 在front_signup.js文件中调用sign = md5()验证表单信息.


# @common_bp.route("/sms_captcha/", methods=['POST'])
# def sms_captcha():
#     telephone = request.form.get('telephone')  # 表单信息收集
#
#     if not telephone:
#         return "请填写手机号"  # 手机信息不存在，输出错误
#
#     # captcha = Captcha.gene_text(number=4)  # 生成4位验证码,这里生成的是验证码，要发送到手机端的，不能是图形验证码
#     captcha = get_random_captcha(num=6)     #或者使用utils/random_captcha.py文件中的随机生成验证码
#
#     # 调用send_telephone_msg.py中send_phone_msg方法发送4位验证码到手机中
#     if send_message(telephone, captcha, ttl=3) == 0:  # 返回成功的状态码为 0
#         return '手机号验证码发送成功'
#     else:
#         return "手机验证码发送失败"


@common_bp.route("/sms_captcha/", methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)  # 收集form表单信息
    if form.validate():  # 表单信息存在
        telephone = form.telephone.data
        captcha = '%06d' % randint(0, 999999)
        print(f'您好，您的短信验证码为{captcha}')
        #if send_message(telephone, captcha, ttl=3) == 0:  # 返回成功的状态码为 0
        if 0 == 0:  # 返回成功的状态码为 0
            try:
                redis_captcha.redis_set(telephone, captcha)
            except:
                print('Redis存储短信验证码错误')
                return restful.params_error(message="短信发送失败")
            return restful.success()
    else:
        return  restful.params_error(message="表单参数错误")
