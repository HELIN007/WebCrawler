# -*- coding=utf-8 -*-
# Python 3.6

import codecs
import simplejson as json
import requests
import time
import pathlib


def download(name, img_link):
    path = 'picture/'
    with codecs.open(path + name, 'wb') as img:
        img.write(requests.get(img_link).content)

def read_and_download():
    path = 'picture/'
    with codecs.open('games.json', 'r', 'utf-8') as f:
        game_list = json.load(f)
        # len(game_list)可以得到长度
        for id, item in enumerate(game_list, start=1):
            # name.append(item["title"].replace('/', ' ') + '.jpg')
            # img_link.append(item["img_link"])
            name = item["title"].replace('/', ' ') + '.jpg'
            img_link = item["img_link"]
            if pathlib.Path(path + name).exists():
                print('已存在 %s' % name)
            else:
                download(name, img_link)
            print('下载完第 %d 个...' % id)

def main():
    t0 = time.time()
    read_and_download()
    t1 = time.time() - t0
    print('下载完成！总共使用%f秒' % t1)


if __name__ == '__main__':
    main()
