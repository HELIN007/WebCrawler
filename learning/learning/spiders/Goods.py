# -*- coding: utf-8 -*-
"""
利用Selenium滚动爬取全部内容，翻页是靠网址实现
"""
import scrapy
from learning.items import GoodsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class GoodsSpider(scrapy.Spider):
# class GoodsSpider(CrawlSpider):
    name = 'goods'
    allowed_domains = ['jd.com']

    # 方法一
    start_urls = []
    # start_requests重写了初始urls，所以不会从start_urls里面读取数据了
    def start_requests(self):
        urls = ['https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={0}'.format(2*i-1)
                for i in range(1, 2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        goods = response.css('#J_goodsList .gl-warp .gl-item')
        for good in goods:
            item = GoodsItem()
            item['name'] = good.css('.p-name a::attr(title)').extract_first()
            item['price'] = '￥' + good.css('.p-price strong i::text').extract_first()
            # if good.css('.p-img img::attr(src)').extract_first() is not None:
            #     item['urls'] = 'https:' + good.css('.p-img img::attr(src)').extract_first()
            # else:
            #     item['urls'] = 'https:' + good.css('.p-img img::attr(data-lazy-img)').extract_first()
            item['img_urls'] = ['https:' + good.css('.p-img img::attr(src)').extract_first()
                            if good.css('.p-img img::attr(src)').extract_first() is not None
                            else 'https:' + good.css('.p-img img::attr(data-lazy-img)').extract_first()]
            yield item

    """
    # 方法二
    # 不知道为什么不能爬到所有的网址
    allowed_domains = ['rakuten.co.jp']
    start_urls = ['https://search.rakuten.co.jp/search/mall/python/?p=1']
    rules = [
        Rule(LinkExtractor(allow=('\?p=\d+')), callback='parse_item')
    ]

    def parse_item(self, response):
        print(response.url)
        # goods = response.css('.main .content .dui-cards .searchresultitem')
        # item = GoodsItem()
        # for good in goods:
        #     item['name'] = good.css('.title a::text').extract_first()
        #     yield item
    """
