# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItcastItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 老师姓名
    title = scrapy.Field()  # 老师职称
    info = scrapy.Field()  # 老师简介


class TencentItem(scrapy.Item):
    id = scrapy.Field()
    post_id = scrapy.Field()
    recruit_post_id = scrapy.Field()
    recruit_post_name = scrapy.Field()
    country_name = scrapy.Field()
    location_name = scrapy.Field()
    bg_name = scrapy.Field()
    product_name = scrapy.Field()
    category_name = scrapy.Field()
    responsibility = scrapy.Field()
    last_update_time = scrapy.Field()
    post_url = scrapy.Field()
    source_id = scrapy.Field()
    is_collect = scrapy.Field()
    is_valid = scrapy.Field()
