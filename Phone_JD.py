# -*- coding=utf-8 -*-
# Python 3.6

import simplejson as json
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

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
    products = []
    if num:
        products_length = 0
        for i in range(num):
            html = browser.page_source  # 获取当前网页的html源码
            doc = pq(html)  # 初始化，导入html，然后在doc里面查找内容
            items = doc('#plist .gl-warp .gl-item').items()  # 找出'#plist .gl-warp .gl-item'下面的所有内容
            for id, item in enumerate(items, start=1):  # 遍历挑出的内容
                product = {
                    'id': id + products_length,
                    'price': item.find('.p-price').text(),
                    'title': item.find('.p-img .err-product').attr('alt'),
                    'img_link': 'https:' + item.find('.p-img .err-product').attr('src')
                                if item.find('.p-img .err-product').attr('src') is not None
                                else 'https:' + item.find('.p-img .err-product').attr('data-lazy-img')
                }
                products.append(product)
            products_length = len(products)
            if i != num -1:  # 点击下一页
                next = browser.find_element_by_class_name('pn-next')
                next.click()
    with codecs.open('text.json', 'w', 'utf-8') as f:  # 将爬取内容写入json文件
        json.dump(products, f, ensure_ascii=False, sort_keys=True, indent=4 * ' ')

def main():
    url = 'https://coll.jd.com/list.html?sub=22575&page=1'
    search_url(url)
    parse_page(num=4)


if __name__ == '__main__':
    main()
