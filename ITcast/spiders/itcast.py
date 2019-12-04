# -*- coding: utf-8 -*-
import scrapy

from ITcast.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['http://www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#']

    def parse(self, response):
        # node_list = response.xpath("//div[@class='li_txt']")  # 使用 xpath
        node_list = response.css(".li_txt")
        for node in node_list:
            item = ItcastItem()
            # 使用 xpath
            # item['name'] = node.xpath('./h3/text()').extract()[0]
            # item['title'] = node.xpath('./h4/text()').extract()[0]
            # item['info'] = node.xpath('./p/text()').extract()[0]

            # 使用 css 选择器
            item['name'] = node.css('h3::text').extract()[0]
            item['title'] = node.css('h4::text').extract()[0]
            item['info'] = node.css('p::text').extract()[0]

            print(item['name'])
            print(item['title'])
            print(item['info'])
            yield
