# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
# 前端的蓝图文件  类视图函数写在这里
from flask import Blueprint

front_bp = Blueprint("front", __name__,)    # 前端不用前缀，直接在首页显示

from . import views