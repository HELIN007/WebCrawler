# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import pymongo
import simplejson as json
import os
import codecs
import requests
import pathlib


class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 可以根据item的内容去重
        self.db['meizi'].update({'img_urls': item['img_urls']}, {'$set': dict(item)}, True)
        # 不去重直接插入数据
        # self.db['all_goods'].insert(dict(item))
        return item


# 可以写入json，但是是一条一条的，不是一个list
class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('games.json', 'w', 'utf-8')

    def process_item(self, item, spider):
        # 生成之后自己加个中括号
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True, indent=4 * ' ') + ',' + '\n'
        self.file.write(line)
        return item


# 无法下载，奇怪的很
class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['img_urls']:
            # yield Request(image_url, meta={'item': item})
            yield Request(image_url)

    def item_completed(self, results, item, info):
        img_paths = [x['path'] for ok, x in results if ok]
        if not img_paths:
            raise DropItem('This url has no images!')
        print('正在下载:', item['name'])
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        img_name = request.url.split('/')[-1]
        # img_name = item.split(' ')[0]
        filename = 'img/{0}'.format(item['name'].replace('/', ''))
        return filename


# 能下载，但国内的网址感觉需要代理
class ImagePipeline(object):
    def process_item(self, item, spider):
        for img_url in item['img_urls']:
            # dir_path = './games/'
            # dir_path = './goods/'
            # if not os.path.exists(dir_path):
            #     os.makedirs(dir_path)
            folder = item['name'].replace('/', '').replace(' ', '')
            dir_path = './meizi/'
            path = dir_path + folder
            if not os.path.exists(path):
                os.makedirs(path)
            # 这样建文件夹会报错
            # img_name = '/{0}/{1}'.format(folder, img_url.split('/')[-1])
            img_name = img_url.split('/')[-1]
            # img_name = item['name'].replace('/', '_') + '.jpg'
            img_path = path + '/' + img_name
            # img_path = dir_path + img_name
            if pathlib.Path(img_path).exists():
                print('{0}已存在'.format(img_name))
            else:
                with codecs.open(img_path, 'wb') as img:
                    print('正在下载{0}'.format(img_name))
                    img.write(requests.get(img_url).content)


class LearningPipeline(object):
    def process_item(self, item, spider):
        return item
