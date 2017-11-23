# -*- coding=utf-8 -*-
# Python 3.6

import re
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_page(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                                 'Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?>(.*?)</a>'
                         +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>'
                         +'.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        # yield {
        #     'index': item[0],
        #     'title': item[1],
        #     'actor': item[2].strip()[3:],
        #      'time': item[3][5:],
        #     'score': item[4]+item[5]
        # }
        yield [item[0], item[1], item[2].strip()[3:], item[3][5:], item[4]+item[5]]

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
