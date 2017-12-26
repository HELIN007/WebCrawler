# -*- coding: utf-8 -*-
"""
适合有规律的网址，使用CrawlSpider, Rule
"""
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from learning.items import MeiziItem


class TestSpider(CrawlSpider):
    name = 'meizi'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/']
    rules = [
        # 没有follower=True的话，就跟进此链接从里面继续爬去符合要求的链接；没有callback的话默认follower=True
        Rule(LinkExtractor(allow=('/a/more_\d\.html'))),
        Rule(LinkExtractor(allow=('/a/\d{0,10}\.html')),
             callback='parse_item')
    ]

    def parse_item(self, response):
        # print(response.url)
        item = MeiziItem()
        item['urls'] = response.url
        item['name'] = response.css('.metaRight a::text').extract_first()
        item['img_urls'] = response.css('.postContent img::attr(src)').extract()
        yield item
