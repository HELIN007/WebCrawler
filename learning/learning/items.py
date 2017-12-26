# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GamesItem(scrapy.Item):
    name = scrapy.Field()
    img_urls = scrapy.Field()
    time = scrapy.Field()
    shop = scrapy.Field()
    version = scrapy.Field()


class GoodsItem(scrapy.Item):
    name = scrapy.Field()
    img_urls = scrapy.Field()
    price = scrapy.Field()


class MeiziItem(scrapy.Item):
    urls = scrapy.Field()
    name = scrapy.Field()
    img_urls = scrapy.Field()


class LearningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
