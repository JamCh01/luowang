#-*-coding:utf-8-*-
#!/usr/bin/env python
# Created by Jam on 2016/9/13.

import requests
import time
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


def mkdir(name):
    if os.path.exists(name):
        pass
    else:
        os.makedirs(name)
    print os.getcwd()
    os.chdir(name)


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
                name = 'vol%s ' % (page_id) + img_url['alt']
                print name
                mkdir(name)
                r = requests.get(img_url['src'])
                with open(img_url['alt'] + '.jpg', 'wb') as img:
                    img.write(r.content)
            except Exception as e:
                print str(e)

        for i in work_queue:
            download(i)
            os.chdir('../')

    def stop(self):
        self.stopped = True

    def is_stoped(self):
        return self.stopped


class song(img):

    def __init__(self):
        super(img, self).__init__()

    def run(self):
        def download(page_id):
            _ua = random.choice(ua.user_agent)
            headers = {
                'User-Agent': _ua
            }
            soup = page_source(page_id)
            title = soup.find('title').text
            title = 'vol%s ' % (page_id) + title.split('-')[0]
            print title
            mkdir(title)
            songs = soup.find_all(
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
                        time.sleep(1)
                    except Exception as e:
                        print str(e)
                        with open(song + '.mp3', 'wb') as song:
                            song.write(r.content)
        for i in work_queue:
            download(i)
            os.chdir('../')

    def stop(self):
        self.stopped = True

    def is_stoped(self):
        return self.stopped

thread1 = img()
thread1.start()
thread1.join()
thread1.stop()
thread0 = song()
thread0.start()
thread0.join()
thread0.stop()