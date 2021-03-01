# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# 定义后端用户模型
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 导入密码加密解密方法的库


class CMS_User(db.Model):
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键  自增
    username = db.Column(db.String(150), nullable=False)  # 非空
    # password = db.Column(db.String(150), nullable=False)
    _password = db.Column(db.String(150), nullable=False)  # 密码加密操作修改字段
    email = db.Column(db.String(50), nullable=False, unique=True)  # 非空、唯一
    join_time = db.Column(db.DateTime, default=datetime.now)  # 默认当前时间

    # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # 调用该方法 返回下面的self._password数值，
        self.email = email

    # 密码加密操作
    @property
    def password(self):  # 密码取值
        return self._password

    @password.setter  # 密码加密  xxx.setter需要和上面的方法名称相同
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)
    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result

    # 封装用户的权限
    @property
    def permission(self):
        if not self.roles:  # 反向查询属性,backref="roles"，
            return 0  # 没有任何权限

        # 所有权限
        all_permissions = 0

        for role in self.roles:  # 循环调用所有角色
            permissions = role.permission  # 将这个角色的权限都取出来  role.permission代表CMSRole中的属性
            all_permissions |= permissions  # 当前这个角色的权限都在all_permissions
        return all_permissions

    # 判断用户所具有的权限
    def has_permissions(self, permission):
        all_permissions = self.permission  # 调用permission(self)方法
        #  若所有权限0b11111111 & 用户权限     等于 本身，则代表具有该权限
        result = all_permissions & permission == permission
        # print(result)
        return result

    # 判断是否是开发人员
    @property
    def is_developer(self):
        return self.has_permissions(CMSPersmission.ALL_PERMISSION)  # 调用has_permissions方法并传入所有权限


# 权限定义，不是模型，没有继承db.Model
class CMSPersmission(object):
    # 255 二进制表示所有的权限
    ALL_PERMISSION = 0b11111111  # 每一位数代表一个权限，共7个权限，8位1个字节
    # 访问权限
    VISITOR = 0b00000001
    # 管理帖子
    POSTER = 0b00000010
    # 管理评论
    COMMENTER = 0b00000100
    # 管理板块
    BOARDER = 0b00001000
    # 管理后台用户
    CMSUSER = 0b00010000
    # 管理前台用户
    FRONTUSER = 0b00100000
    # 管理管理员用户
    ADMINER = 0b01000000


# 权限与角色是多对多的关系，创建他们的中间表
cms_role_user = db.Table(
    "cms_role_user",
    db.Column("cms_role_id", db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column("cms_user_id", db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
)


# 角色模型定义   继承db.Model
class CMSRole(db.Model):
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键  自增
    name = db.Column(db.String(50), nullable=False)  # 非空
    desc = db.Column(db.String(250), nullable=False)  # 非空
    creat_time = db.Column(db.DateTime, default=datetime.now)
    permission = db.Column(db.Integer, default=CMSPersmission.VISITOR)  # 默认先给游客权限

    # 反向查询属性,关联中间表secondary=cms_role_user,对应了CMS_User模型,建立模型联系,不映射到数据库中
    users = db.relationship('CMS_User', secondary=cms_role_user, backref="roles")  # roles是CMS_User的外键
