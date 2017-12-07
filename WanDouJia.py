# -*- coding=utf-8 -*-
# Python 3.6

import time
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from multiprocessing.pool import Pool

def get_url(page):
    """
    :param page: 所需爬取的页数
    :return: 返回爬取的url
    """
    url = 'http://www.wandoujia.com/api/top/more?resourceType=1&page={0}&ctoken=eTqgvXhGnzMEf5b14dIzwdj-web'.format(page)
    # url = 'http://www.wandoujia.com/top/game'  # 渲染过后的网址
    return url

def parse_page(url):
    """
    :param url: 传入url
    :return: 返回每页爬取的数量
    """
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                                 'Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            titles = soup.select('h2')
            num = len(titles)  # 可以返回长度
            # 此次返回的json数据，所以注释的代码查找不到所需的内容，如果返回的是渲染过的网址则可以精确查找
            # titles = soup.find_all(class_="app-title-h2")
            # titles = soup.select('h2[class="app-title-h2"]')
            # titles = soup.select('a[class="name"]')
            # for id, title in enumerate(titles, start=1):
                # print(id, title.text.replace('\\n', '').replace(' ', ''))
                # print(title.text.strip())
                # print(title.get('href'))
            for title in titles:
                print(title.text.replace('\\n', '').replace(' ', ''))
            return num
    except RequestException:
        print('请求网站失败！')


def main():
    urls = []
    page = 10  # 爬取的页数
    # 获取网址
    for i in range(page):
        urls.append(get_url(i))
    # 多进程爬取
    t0 = time.time()
    pool = Pool(processes=4)
    result1 = pool.map(parse_page, urls)
    pool.close()
    pool.join()
    t1 = time.time() - t0
    # 非多进程爬取
    result2 = []
    for url in urls:
        result2.append(parse_page(url))
    t2 = time.time() - t1 -t0
    print('多进程所需: ', t1)
    print('非多进程所需: ', t2)
    print('多进程每页输出爬取数量: ', result1)
    print('非多进程每页输出爬取数量: ', result2)


if __name__ == '__main__':
    main()
