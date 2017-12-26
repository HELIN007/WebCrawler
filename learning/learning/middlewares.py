# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from logging import getLogger
import time


class GamesMiddleware():
    def __init__(self, timeout=30, service_args=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        # 使用webdriver.PhantonJS的话好像得手工关掉进程
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, self.timeout)

    # 不知道为什么不执行
    # def __del__(self):
    #     if self.driver is not None:
    #         self.driver.quit()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        for i in range(22):
            try:
                next = self.driver.find_element_by_xpath('//*[@id="soft-search"]/div/div[6]/i')
                next.click()
                time.sleep(1)
            except:
                print('已经到达最后一页啦！')
                break
        html = self.driver.page_source.encode('utf-8')
        self.driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=html, request=request)

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
    #                service_args=crawler.settings.get('CHROME_SERVICE_ARGS'))


class GoodsMiddleware(object):
    def __init__(self, timeout=30, service_args=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, self.timeout)

    # 不知道为什么不执行
    # def __del__(self):
    #     if self.driver is not None:
    #         self.driver.quit()

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            try:
                for i in range(3):
                    next_page = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # 不设时延的话可能会被屏蔽，或者爬取不到内容，做一个有道德的爬者
                    time.sleep(2)
            except:
                print('已经翻到底啦！')
                return
            html = self.driver.page_source.encode('utf-8')
            time.sleep(1)
            return HtmlResponse(request.url, encoding='utf-8', body=html, request=request)
        except TimeoutError:
            pass


"""
class LearningSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
"""
