# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# 导入蓝图
from flask_mail import Message

from utils import random_captcha
from . import cms_bp
# 蓝图文件：实现模块化应用，应用可以分解成一系列的蓝图   后端的类视图函数写在这个文件
from flask import render_template, views, session, jsonify  # 定义类视图，显示模板文件
from flask import request, redirect, url_for, g  # 页面跳转redirect   request请求收集
# 导入form表单   .forms代表同级目录下的forms.py
from .forms import LoginForm
from .forms import ResetPwdForm
# 导入模型  .models代表同级目录下的models.py
from .models import CMS_User, CMSPersmission
from .decorators import permission_required  # 传参装饰器验证用户不同模块权限

from exts import db, mail


# 首页显示
@cms_bp.route("/")
def index():
    return render_template('cms/cms_index.html')


# 定义类视图，显示模板文件
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    # 用户登录操作验证
    def post(self):
        # 收集表单信息
        login_form = LoginForm(request.form)
        if login_form.validate():
            # 数据库验证
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data

            # 查询数据库中的用户信息
            user = CMS_User.query.filter_by(email=email).first()  # 邮箱唯一，用于查询验证用户
            if user and user.check_password(password):  # 验证用户和密码是否都正确
                session['user_id'] = user.id  # 查询到用户数据时，保存session的id到浏览器
                if remember:  # 如果用户点击了remember选择，在浏览器中进行数据持久化
                    session.permanent = True  # 数据持久化，默认31天，需要设置session_key在config.py中
                # 登录成功，跳转到后台首页
                return redirect(url_for('cms.index'))  # 在蓝图中必须加cms   跳转到index方法
            else:
                # return "邮箱或密码错误"  # 登录出错，返回结果
                return self.get(message=login_form.get_err())
        else:
            return self.get(message=login_form.get_err())


# 用户注销登录
@cms_bp.route("/logout/")  # 需要关联到cms/cms_index.html中的注销属性
def logout():
    # session清除user_id
    del session['user_id']
    # 重定向到登录界面
    return redirect(url_for('cms.login'))  # 重定向(redirec)为把url变为重定向的url


# 定义个人中心的路由
@cms_bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html")  # 模板渲染(render_template)则不会改变url，模板渲染是用模板来渲染请求的url


# 修改密码的类视图验证
class ResetPwd(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpwd.html')  # 模板渲染到cms_resetpwd.html

    # post提交密码修改
    def post(self):
        # 先审查旧密码是否与数据库中的信息相同
        reser_pwd_form = ResetPwdForm(request.form)
        if reser_pwd_form.validate():
            oldpwd = reser_pwd_form.oldpwd.data
            newpwd = reser_pwd_form.newpwd.data
            # 对象
            user = g.cms_user
            # 将用户输入的密码进行加密检测是否与数据库中的相同
            if user.check_password(oldpwd):
                # 更新我的密码  将新密码赋值，此时的新密码已经经过验证二次密码是否一致
                user.password = newpwd  # user.password已经调用了models.py中的 @property装饰器进行密码加密
                # 数据库更新
                db.session.commit()
                return jsonify({"code": 400, "message": "密码修改成功"})
            else:
                # 当前用户输入的旧密码与数据库中的不符
                return jsonify({"code": 400, "message": "旧密码输入错误"})
        else:
            # ajax 需要返回一个json类型的数据
            message = reser_pwd_form.get_err()  # 收集错误信息
            return jsonify({"code": 400, "message": message})  # 将数据转换成json类型


# 定义修改邮箱的类视图 验证
class ResetEmail(views.MethodView):
    def get(self):
        return render_template("cms/cms_resetemail.html")  # 返回到修改邮箱页面url

    def post(self):
        print('POST修改邮箱')
        return 'POST修改邮箱'


# 发送测试邮件进行验证
@cms_bp.route("/send_email/")
def send_mail():
    message = Message('邮件发送', recipients=['1536452582@qq.com'], body='测试邮件发送')  # 主题：邮件发送;收件人：recipients;邮件内容：测试邮件发送
    mail.send(message)  # 发送邮件
    return "邮件已发送"


# 邮件发送
class EmailCaptcha(views.MethodView):
    def get(self):  # 根据resetemail.js中的ajax方法来写函数，不需要post请求
        email = request.args.get('email')  # 查询email参数是否存在
        if not email:
            return '请传递邮箱参数'

        # 发送邮件，内容为一个验证码：4、6位数字英文组合
        captcha = random_captcha.get_random_captcha(4)  # 生成4位验证码
        # message = Message('BBS论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
        message = 'BBS论坛邮箱验证码:您的验证码是：%s' % captcha
        print(message)
        # # 异常处理
        # try:
        #     mail.send(message)
        # except:
        #     return "服务器错误，邮件验证码未发送！"  # 发送异常，服务器错误

        # 验证码保存，一般有时效性，且频繁请求变化，所以保存在Redis中
        return "邮件验证码发送成功！"


# 轮播图管理路由
@cms_bp.route("/banners/")
def banners():
    return render_template("cms/cms_banners.html")


# 帖子管理路由 ，需要和cms_base.js中命名的相同才可以
@cms_bp.route("/posts/")
@permission_required(CMSPersmission.POSTER)  # 传参装饰器验证不同用户不同模块权限
def posts():
    return render_template("cms/cms_posts.html")


# 评论管理路由
@cms_bp.route("/comments/")
@permission_required(CMSPersmission.COMMENTER)  # 传参装饰器验证不同用户不同模块权限
def comments():
    return render_template("cms/cms_comments.html")


# 板块管理路由
@cms_bp.route("/boards/")
@permission_required(CMSPersmission.BOARDER)  # 传参装饰器验证不同用户不同模块权限
def boards():
    return render_template("cms/cms_boards.html")


# 前台用户管理路由
@cms_bp.route("/fusers/")
@permission_required(CMSPersmission.FRONTUSER)  # 传参装饰器验证不同用户不同模块权限
def fuser():
    return render_template("cms/cms_fuser.html")


# 后用户管理路由
@cms_bp.route("/cusers/")
@permission_required(CMSPersmission.CMSUSER)  # 传参装饰器验证不同用户不同模块权限
def cuser():
    return render_template("cms/cms_cuser.html")


# 添加登录路由
cms_bp.add_url_rule("/login/", view_func=LoginView.as_view('login'))  # view_func 命名操作名字，"/login/"路由地址
# 类视图函数添加绑定路由  注意类视图需要修改ResetPwd.as_view('resetpwd')
cms_bp.add_url_rule("/resetpwd/", view_func=ResetPwd.as_view('resetpwd'))  # view_func 命名操作名字，/resetpwd/路由地址
# 添加修改邮箱的类视图路由绑定，路由的命名和cms_base.js中的命名要相同，否则不关联，url=/resetemail/必须要和resetemail.js中的ajax绑定的路由相同
cms_bp.add_url_rule("/resetemail/", view_func=ResetEmail.as_view('resetemail'))
# 绑定路由，路由的命名和cms_base.js中的命名要相同，必须要和resetemail.js中的ajax绑定的路由相同
cms_bp.add_url_rule("/email_captcha/", view_func=EmailCaptcha.as_view('email_captcha'))
