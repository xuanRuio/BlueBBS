# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
from io import BytesIO

from flask import render_template, views, make_response, request, session

from utils import restful, redis_captcha, safe_url
from utils.captcha import Captcha
from . import front_bp
from .forms import SignupForm, SigninForm
from .models import Front_User
from exts import db


@front_bp.route("/")
def index():
    return render_template("front/front_index.html")


# 图形验证码路由
@front_bp.route("/captcha/")
def graph_captcha():
    try:  # 异常处理
        # 图像验证码生成文件中返回两个参数   text, image
        text, image = Captcha.gene_graph_captcha()  # 生成图形验证码，image是二进制数据，需要转换成字节流才能使用
        print('您好，您的图片验证码为%s' % text)
        try:
            # 将图形验证码保存到Redis数据库中
            redis_captcha.redis_set(text.lower(), text.lower())  # redis_set中需要传参key和value，text没有唯一对应的key，只能都传参text
        except:
            print('Redis存储图片验证码错误')
        # BytesIO是生成的字节流
        out = BytesIO()
        image.save(out, 'png')  # 把图片image保存在字节流中，并指定为png格式
        # 文件流指针
        out.seek(0)  # 从字节流最初开始读取
        # 生成response对象，用于返回前端模板中
        resp = make_response(out.read())
        resp.content_type = 'image/png'  # 指定数据类型
    except:
        return graph_captcha()  # 没有生成验证码就再调用一次
    return resp  # 返回对象

# # 测试referrer的跳转
# @front_bp.route("/test/")
# def test():
#     return render_template("front/front_test.html")


# 用户注册类视图
class SingupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        # 确保URL安全的文件：utils/safe_url.py
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):  # 跳转的url不能是当前页面，否则没意义
            return render_template("front/front_signup.html", return_to=return_to)  # return_to渲染到前端界面
        else:
           return render_template("front/front_signup.html")


    def post(self):
        form = SignupForm(request.form)  # 收集表单信息
        print('开始验证')
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            # 前台用户模型数据添加到数据库
            user = Front_User(telephone=telephone, username=username, password=password)
            print('添加用户成功')
            db.session.add(user)
            db.session.commit()  # 提交到数据库

            # 表单验证通过，提交到数据库成功
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())  # 表单信息验证出错


#用户登录的类视图
class SinginView(views.MethodView):
    def get(self):
        return_to = request.referrer  # referrer是上一个url

        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):  # 跳转的url不能是当前页面，判断url是否安全
            return render_template("front/front_signin.html", return_to=return_to)  # return_to渲染到前端界面
        else:
            return render_template("front/front_signin.html")  # 如果没获取url,直接渲染注册界面

    def post(self):
        form = SigninForm(request.form)  # 登录界面的Form表单信息

        if form.validate():  # 表单信息存在
            # 收集form表单信息
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = Front_User.query.filter_by(telephone=telephone).first()  # 通过手机号验证该用户是否存在数据库
            if user and user.check_password(password):  # 判断密码和用户是否正确
                session['user_id'] = user.id  # 用户的id存储到session中，用于登录验证
                if remember:  # 如果remember状态是1
                    # session持久化
                    session.permanent = True
                return restful.success()  # 成功
            else:
                return restful.params_error(message="手机号或者密码错误")  # 密码是、用户不正确
        else:
            return restful.params_error(message=form.get_error())  # 表单信息不存在，输出异常信息


# 绑定类视图的路由
front_bp.add_url_rule("/signup/", view_func=SingupView.as_view("signup"))
front_bp.add_url_rule("/signin/", view_func=SinginView.as_view("signin"))