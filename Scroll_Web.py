# -*- coding=utf-8 -*-
# Python 3.6
# 滚动加载页面

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq
from pprint import pprint

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 30)

def search_url(url):
    """
    :param url: 需要查询的网址
    :return:
    """
    try:
        browser.get(url)
    except TimeoutError:
        return search_url(url)

def parse_page(page):
    """
    :return:
    """
    # 模拟浏览器自动翻页
    for i in range(page):
        next = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 不设时延的话可能会被屏蔽，做一个有道德的爬者
        time.sleep(1)
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainContent .newsbox .news_li').items()
    # 节省内存
    for item in items:
        yield {
            '标题': item.find('h2').text(),
            '时间': item.find('.pdtt_trbs span').eq(0).text(),
            '链接': 'http://www.thepaper.cn/' + str(item.find('.news_tu a').attr('href')),
            '公司': item.find('.pdtt_trbs a').text()
        }

def main():
    url = 'http://www.thepaper.cn/'
    search_url(url)
    page = 30
    for news in parse_page(page):
        pprint(news)
    browser.quit()


if __name__ == '__main__':
    main()
