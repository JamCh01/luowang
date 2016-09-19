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
                    referer = 'http://www.luoo.net/music/'+ str(page_id)
                    headers = {
                        'Host': 'luoo-mp3.kssws.ks-cdn.com',
                        'Proxy-Connection': 'keep-alive',
                        'Accept-Encoding': 'identity;q=1, *;q=0',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                        'Accept': '*/*',
                        'Referer': referer,
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Range': 'bytes=0-'
                    }

                    local_name = song + '.mp3'
                    r = requests.get(url, stream=True)

                    try:

                        with open(local_name,'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()

                        time.sleep(random.randrange(1,2))
                    except Exception as e:
                         print str(e)
                         with open(local_name, 'wb') as song:
                             song.write(r.content)
                    song_num += 1
                    time.sleep(random.randint(1, 10))
        for i in work_queue:
            download(i)
            os.chdir('../')

    def stop(self):
        self.stopped = True

    def is_stoped(self):
        return self.stopped



#thread1 = img()
#thread1.start()
#thread1.join()
#thread1.stop()
thread0 = song()
thread0.start()
thread0.join()
thread0.stop()