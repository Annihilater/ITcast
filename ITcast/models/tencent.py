#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019-05-19 23:41
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : tencent.py
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.dialects.mysql import LONGTEXT


class Tencent:
    # 此为用于 orm 创建 Tencent 数据表的模型
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    url = Column(String(300), nullable=False, default='')
    url_object_id = Column(String(50), nullable=False, default='')
    title = Column(String(200), nullable=False, default='')
    cover_img_url = Column(String(300))
    cover_img_url_path = Column(String(200))
    create_time = Column(Date)
    praise_nums = Column(Integer, nullable=False, default=0)
    fav_nums = Column(Integer, nullable=False, default=0)
    comment_nums = Column(Integer, nullable=False, default=0)
    content = Column(LONGTEXT(), nullable=False, default='')
    copyright_area = Column(String(100))
    tags = Column(String(100))

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
