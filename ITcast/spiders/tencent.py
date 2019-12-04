# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from ITcast.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = [
        'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1558262921715&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        print(response.text)
        data = response.text
        data = json.loads(data)
        data = data['Data']['Posts']
        positions = data
        with open('data/tencent.txt', 'w') as f:
            f.write(str(positions))
        for position in positions:
            item = TencentItem()
            item['id'] = position['Id']
            item['post_id'] = position['PostId']
            item['recruit_post_id'] = position['RecruitPostId']
            item['recruit_post_name'] = position['RecruitPostName']
            item['country_name'] = position['CountryName']
            item['location_name'] = position['LocationName']
            item['bg_name'] = position['BGName']
            item['product_name'] = position['ProductName']
            item['category_name'] = position['CategoryName']
            item['responsibility'] = position['Responsibility']
            item['last_update_time'] = position['LastUpdateTime']
            item['post_url'] = position['PostURL']
            item['source_id'] = position['SourceID']
            item['is_collect'] = position['IsCollect']
            item['is_valid'] = position['IsValid']

            yield item

    # def start_requests(self):
    #     cookie = {}
    #     for url in self.start_urls:
    #         yield Request(url, cookies=cookie)
