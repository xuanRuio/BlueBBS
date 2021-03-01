# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""

from flask_script import Manager
from apps import create_app

app = create_app()
manage = Manager(app)

if __name__ == '__main__':
    print(app.url_map)
    print(app.config)
    manage.run()

