# -*- coding: utf-8 -*-
"""
正常的Scrapy爬虫，需要配合Selenium爬取Ajax网站。
可以下载图片，存成Json文件，存入Mongodb。
"""
import scrapy
from learning.items import GamesItem


class GamesSpider(scrapy.Spider):
    name = 'games'
    allowed_domains = ['www.nintendo.co.jp/']
    start_urls = ['http://www.nintendo.co.jp//']

    def start_requests(self):
        url = 'https://www.nintendo.co.jp/software/switch/index.html'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        games = response.css('#soft-search .ncommon-l-content #soft-search__pool .ncommon-softUnit .ncommon-u-linkbox')
        for game in games:
            item = GamesItem()
            item['name'] = game.css('.ncommon-softUnit__heightbase .ncommon-softUnit__name::text').extract_first()
            item['time'] = game.css('.ncommon-softUnit__sub .ncommon-softUnit__dateAndPrice::text').extract_first()
            item['img_urls'] = [game.css('.ncommon-softUnit__thumb .ncommon-thumb::attr(style)').extract_first()[23:-15]]
            # item['img_urls'] = game.css('.ncommon-softUnit__thumb .ncommon-thumb::attr(style)').extract()
            yield item

