# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
from flask_script import Manager
from bulebbs import app  # 需要将当前文件夹设置为当前根目录，才不会报错
from flask_migrate import Migrate, MigrateCommand
from exts import db

# 导入模型 才能映射到数据库     导入后端的模型
from apps.front.models import Front_User
from apps.cms.models import CMS_User
from apps.cms.models import CMSRole, CMSPersmission

manage = Manager(app)
# 数据库迁移
Migrate(app, db)
manage.add_command('db', MigrateCommand)


# 命令行添加前台用户
@manage.option('-t', '--telephone', dest='telephone')
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = Front_User(telephone=telephone, username=username, password=password)
    # 添加映射到数据库，提交至数据库
    db.session.add(user)
    db.session.commit()
    print("front前台用户添加成功")


# 命令行添加后端用户
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMS_User(username=username, password=password, email=email)
    # 添加映射到数据库，提交至数据库
    db.session.add(user)
    db.session.commit()
    print("cms后端用户添加成功")


@manage.command
def create_role():
    # 访问者
    visitor = CMSRole(name="访问者", desc="只能查看数据，不能修改数据")
    visitor.permission = CMSPersmission.VISITOR  # 权限

    # 运营人员
    operator = CMSRole(name="运营人员", desc="管理评论、帖子、管理前台用户")
    # 权限或运算，代表包含有运算中的所有权限     二进制的运算 001|010=011
    operator.permission = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | \
                          CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER

    # 管理员
    admin = CMSRole(name="管理员", desc="拥有本系统大部分权限")
    admin.permission = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | \
                       CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER | CMSPersmission.BOARDER

    # 开发人员
    developer = CMSRole(name="开发人员", desc="拥有本系统所有权限")
    developer.permission = CMSPersmission.ALL_PERMISSION

    # 提交数据库   添加身份字段到数据库中的表,
    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    return "创建角色成功"


# 测试用户权限
@manage.command
def test_permission():
    # user = CMS_User.query.first()                          # 查询第一个用户，当时创建的用户还没有关联权限，所以应该是没有权限
    user = CMS_User.query.get(2)
    print(user)  # 显示用户信息
    if user.has_permissions(CMSPersmission.VISITOR):  # has_permissions方法判定是否具有该权限
        print("这个用户有访问者的权限！")
    else:
        print("这个用户有访问者的权限！")


# 添加用户到角色里面
@manage.option("-e", "--email", dest="email")
@manage.option("-n", "--name", dest="name")
def add_user_to_role(email, name):
    user = CMS_User.query.filter_by(email=email).first()  # 通过邮箱查询用户
    if user:
        role = CMSRole.query.filter_by(name=name).first()  # 邮箱存在的前提下，通过name查询角色
        if role:
            role.users.append(user)  # 将用户添加到角色中，list类型数据，role.users是CMSRole中的外键
            db.session.commit()  # 映射到数据库
            print("用户添加到角色成功")
        else:
            print("该角色不存在")
    else:
        print("邮箱不存在")


if __name__ == '__main__':
    manage.run()
