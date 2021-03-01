# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
from flask import Flask
from flask_wtf import CSRFProtect

import config
from apps.cms import cms_bp
from apps.common import common_bp
from apps.front import front_bp
from exts import db, mail

# 蓝图列表
bps = [
    cms_bp,
    front_bp,
    common_bp,
]
# 工厂函数
def create_app():
    # 实例化Flask对象：
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    CSRFProtect(app)
    # 加载配置信息：
    app.config.from_object(config)
    # app数据库初始化：
    db.init_app(app)
    mail.init_app(app)
    # 注册蓝图
    for bp in bps:
        app.register_blueprint(bp)
    return app