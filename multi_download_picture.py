# -*- coding=utf-8 -*-
# Python 3.6

import codecs
import simplejson as json
import requests
import time
import pathlib
from multiprocessing.pool import Pool
from multiprocessing import cpu_count  # 查看电脑核数


def download(name, img_link):
    path = 'picture/'
    if pathlib.Path(path + name).exists():
        print('已存在 %s' % name)
        # print('已存在！')
    else:
        print('正在爬取 %s' % name)
        with codecs.open(path + name, 'wb') as img:
            img.write(requests.get(img_link).content)
    return "完成 %s" % name

def read_and_download():
    names = []
    img_links = []
    with codecs.open('games.json', 'r', 'utf-8') as f:
        game_list = json.load(f)
        # len(game_list)可以得到长度
        for id, item in enumerate(game_list, start=1):
            names.append(item["title"].replace('/', ' ') + '.jpg')
            img_links.append(item["img_link"])
    # name_link = [(name, img_link) for name in names for img_link in img_links]
    name_link = zip(names, img_links)
    return name_link

def main():
    t0 = time.time()
    name_link = read_and_download()
    pool = Pool(processes=cpu_count())
    # 传入多参数数时改成元组，和使用starmap及starmap_async
    result = pool.starmap_async(download, name_link)  # 异步非阻塞，一次只传入一个值
    # print(result.get())  # 可以查看多进程返回的结果
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 调用join之前，先调用close函数，否则会出错。join函数等待所有子进程结束
    t1 = time.time() - t0
    print(t1)


if __name__ == '__main__':
    main()
