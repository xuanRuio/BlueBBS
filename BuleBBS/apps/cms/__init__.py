# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# 蓝图文件：实现模块化应用，应用可以分解成一系列的蓝图
# 后端的类视图函数写在这个文件
from flask import Blueprint

cms_bp = Blueprint("cms", __name__, url_prefix='/cms/',)     # URL前缀url_prefix
# 导入钩子函数
from .hooks import before_request

from . import views