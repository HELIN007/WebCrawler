# -*- coding=utf-8 -*-
# Python 3.6
# 这个例子个人感觉不适合多进程爬取，可能我的写法有问题吧
# 一旦开启多进程有时会过快翻页，导致那页的内容未能爬取到


import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        time.sleep(3)
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#mq'))
        )
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#J_PopSearch > div.sb-search > div > form > input[type="submit"]:nth-child(2)'))
        )
        input.send_keys('iPhone')
        submit.click()
        total = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#mainsrp-pager > div > div > div > div.total'))
        )
        return total.text
    except TimeoutError:
        return search_url(url)

def get_things(page_num):
    try:
        if page_num:
            length = 0
            products = []
            for i in range(1, page_num + 1):
                # 找到输入框的位置
                input = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        '#mainsrp-pager > div > div > div > div.form > input'))
                )
                # 找到搜索的位置
                submit = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
                )
                # 先清空输入框，再输入想输的内容
                input.clear()
                input.send_keys(i)
                # 点击搜索
                submit.click()
                # 直到翻页输入框的数字和当前页数一致，开始下面的步骤
                wait.until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                          '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
                                                          str(i))
                )
                print('正在爬取第%s页' % i)
                html = browser.page_source
                doc = pq(html)
                items = doc('#mainsrp-itemlist .items .item').items()
                for id, item in enumerate(items, start=1):
                    # print(id, item.find('.ctx-box .price').text())
                    print(id + length, item.find('.ctx-box .J_ClickStat').text())
                    # print(id, 'http:' + str(item.find('.pic .img').attr('src')))
                    products.append(item.find('.ctx-box .J_ClickStat').text())
                length = len(products)
                time.sleep(1)  # 不设时延有时爬取过快会出错
    except TimeoutError:
        get_things(page_num)

"""
def parse_page():
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for id, item in enumerate(items, start=1):
        # print(id, item.find('.ctx-box .price').text())
        print(id, item.find('.ctx-box .J_ClickStat').text())
        # print(id, 'http:' + str(item.find('.pic .img').attr('src')))
"""

def main():
    url = 'https://world.taobao.com/'
    # pages写着玩
    pages = int(re.compile('(\d+)').search(search_url(url)).group(0))
    t0 = time.time()
    # get_things(pages)
    get_things(5)
    t1 = time.time() - t0
    print(t1)
    browser.quit()


if __name__ == '__main__':
    main()
