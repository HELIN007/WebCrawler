# -*- coding=utf-8 -*-
# Python 3.6

import re
import simplejson as json
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from pyquery import PyQuery as pq
import time

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

def parse_page(num):
    """
    :param num: 所需爬取的页数
    :return:
    """
    t0 = time.time()
    games = []
    if num:
        products_length = 0
        # 没有下一页，url不发生变化
        try:
            for i in range(num):
                next = browser.find_element_by_xpath('//*[@id="soft-search"]/div/div[6]/i')
                next.click()
                time.sleep(1)  # 设置时延，做一个有道德的爬虫
        except ElementNotVisibleException:
            print('开始爬取，正在写入中...')
        html = browser.page_source  # 获取当前网页的html源码
        doc = pq(html)  # 初始化，导入html，然后在doc里面查找内容
        items = doc('#soft-search__pool .ncommon-grid__col .ncommon-softUnit .ncommon-u-linkbox').items()  # 找出下面的所有内容
        for id, item in enumerate(items, start=1):  # 遍历挑出的内容
            product = {
                'id': id,
                'title': item.find('.ncommon-softUnit__heightbase .ncommon-softUnit__main').text(),
                'time': item.find('.ncommon-softUnit__sub .ncommon-softUnit__dateAndPrice').text().replace(' ', ''),
                'shop': item.find('.ncommon-softUnit__sub .ncommon-softUnit__company').text(),
                'version': item.find('.ncommon-softUnit__sub .ncommon-softUnit__type').text(),
                'img_link': item.find('.ncommon-softUnit__thumb .ncommon-thumb').attr('style')[23:-15]
                # 'img_link': re.findall(re.compile('url\("(.*?)\?', re.S), item.find('.ncommon-softUnit__thumb .ncommon-thumb').attr('style'))
            }
            games.append(product)
    with codecs.open('games.json', 'w', 'utf-8') as f:  # 将爬取内容写入json文件
        json.dump(games, f, ensure_ascii=False, sort_keys=True, indent=4 * ' ')
    t = time.time() - t0
    print('全部爬取完毕！共花费%f秒。' % t)

def main():
    url = 'https://www.nintendo.co.jp/software/switch/index.html'
    search_url(url)
    parse_page(num=17)
    browser.quit()


if __name__ == '__main__':
    main()
