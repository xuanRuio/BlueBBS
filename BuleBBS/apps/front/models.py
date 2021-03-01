# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# 前台管理的模型
from exts import db  # 数据库连接
import shortuuid  # 前台用户id加密
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 导入密码加密，解密方法的库
import enum  # 导入枚举


# 性别选择的类
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


#   前台用户模型类
class Front_User(db.Model):
    __tablename__ = "front_user"
    # id 类型不用db.Integer类型，使用String是为了防止爆破，同时使用shortuuid进行加密
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)  # 非空唯一
    username = db.Column(db.String(150), nullable=False)
    _password = db.Column(db.String(150), nullable=False)  # 密码加密操作修改字段
    email = db.Column(db.String(50), unique=True)

    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(150))  # 头像，二进制数据
    signatrue = db.Column(db.String(500))  # 签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)  # 性别枚举类，默认未知
    join_time = db.Column(db.DateTime, default=datetime.now)  # 默认当前时间

    # 修改密码加密操作，manage.py映射数据库时候，使用字段保持相同，由于字段太多，使用传参形式
    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:  # 如果传参中包含有
            self.password = kwargs.get('password')  # 获取该参数值赋值给password
            kwargs.pop('password')  # 模型参数中是_password，不是password，弹出

        # super(FrontUser, self).__init__(*args, **kwargs)   # python2的写法
        super().__init__(*args, **kwargs)

    # 密码加密操作
    @property
    def password(self):  # 密码取值
        return self._password

    @password.setter  # 密码加密
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    # 用于验证前台登录密码是否和数据库一致，raw_password是前台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)  # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result