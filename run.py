#-*-coding:utf-8-*-
#!/usr/bin/env python
# Created by Jam on 2016/9/13.

import requests
import threading
import os
import random
import ua
from bs4 import BeautifulSoup


def max_num():
    r = requests.get(url='http://www.luoo.net/music/')
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf8')
    node = soup.find('div', {'class': 'item'})
    _max = node.find('a')['href'].split('/')[-1]
    return _max

max_num = max_num()
work_queue = range(1, int(max_num) + 1)


def page_source(page_id):
    _ua = random.choice(ua.user_agent)
    headers = {
        'User-Agent': _ua
    }
    r = requests.get('http://www.luoo.net/music/' +
                     str(page_id), headers=headers)
    soup = BeautifulSoup(
        r.content,
        'html.parser',
        from_encoding='utf8')
    return soup


class img(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        def download(page_id):
            try:
                img_url = page_source(
                    page_id).find(
                    'img', {
                        'class': 'vol-cover'})
                r = requests.get(img_url['src'])
                with open(img_url['alt'] + '.jpg', 'wb') as img:
                    img.write(r.content)
            except Exception as e:
                print str(e)
        for i in work_queue:
            download(i)


class song(img):

    def __init__(self):
        super(img, self).__init__()

    def run(self):
        def download(page_id):
            _ua = random.choice(ua.user_agent)
            headers = {
                'User-Agent': _ua
            }
            songs = page_source(page_id).find_all(
                'div', {'class': 'player-wrapper'})
            song_list = []
            for song in songs:
                song_info = song.text.strip().replace('\n', '_')
                song_info = song_info.replace(':', '-')
                song_list.append(song_info)
            song_num = 1
            name_reg = ['<', '>', '/', '\\', '|', '\"', '*', '?', '&', '$']
            for song in song_list:
                for i in name_reg:
                    if i in song:
                        song = song.replace(i, '')
                if os.path.exists(song + '.mp3'):
                    pass
                else:
                    url = 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio' + \
                        str(page_id) + '/' + str(song_num) + '.mp3'
                    r = requests.get(url, headers=headers)
                    try:
                        with open(song + '.mp3', 'wb') as song:
                            song.write(r.content)

                    except Exception as e:
                        print str(e)
                        with open(song + '.mp3', 'wb') as song:
                            song.write(r.content)
        for i in work_queue:
            download(i)

thread0 = song()
thread0.start()
