import os
import queue
import logging
import requests
import platform
import threading
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


class common(object):
    '''
    基础页面爬虫
    '''

    def __init__(self):
        self.headers = {
            'Host':
                'www.luoo.net',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.url = ''

    def spider(self):
        s = requests.Session()
        s.mount(prefix=self.url, adapter=HTTPAdapter(max_retries=5))
        r = s.get(url=self.url, headers=self.headers)
        res = (r.text.encode(r.encoding).decode('utf8'))
        soup = BeautifulSoup(res, 'html.parser')
        return soup


class spider4id(common):

    def __init__(self, magazine_id):
        common.__init__(self)
        self.headers['Referer'] = 'http://www.luoo.net/music/'
        self.magazine_id = magazine_id
        self.url = 'http://www.luoo.net/music/%s' % magazine_id


def mp3url(magazine_id):
    # 落网匹配规则
    base_url = 'http://mp3-cdn.luoo.net/low'
    magazine_id = int(magazine_id)
    if magazine_id == 497:
        return '%s/luoo/s1/' % (base_url)

    elif magazine_id >= 498 and magazine_id <= 521:
        return '%s/luoo/S%s/' % (base_url, str(magazine_id - 496))

    elif magazine_id == 522:
        return '%s/luoo/s26/'

    elif magazine_id >= 523 and magazine_id <= 539:
        return '%s/anbai/radio%s/' % (base_url, str(magazine_id - 522))

    elif magazine_id >= 540 and magazine_id <= 543:
        return '%s/china/radio%s/' % (base_url, str(magazine_id - 539))

    elif magazine_id == 545:
        return '%s/china/radio5/' % (base_url)

    elif magazine_id >= 546 and magazine_id <= 557:
        return '%s/world/radio%s/' % (base_url, str(magazine_id - 545))

    elif magazine_id == 558 or magazine_id == 559:
        return '%s/electric/radio%s/' % (base_url, str(magazine_id - 557))

    elif magazine_id == 560 or magazine_id == 561:
        return '%s/classical/radio%s/' % (base_url, str(magazine_id - 559))

    elif magazine_id >= 562 and magazine_id <= 565:
        return '%s/jazz/radio%s/' % (base_url, str(magazine_id - 561))

    elif magazine_id == 569:
        return '%s/electric/radio3/' % (base_url)

    elif magazine_id == 573:
        return '%s/luoo/radio499/' % (base_url)

    elif magazine_id == 576:
        return '%s/jazz/radio5/' % (base_url)

    elif magazine_id == 581:
        return '%s/luoo/radio500/' % (base_url)

    elif magazine_id == 582:
        return '%s/luoo/radio581/' % (base_url)

    elif magazine_id == 583:
        return '%s/anbai/radio18/' % (base_url)

    elif magazine_id == 594:
        return '%s/anbai/radio19/' % (base_url)

    else:
        return '%s/luoo/radio%s/' % (base_url, magazine_id)


download_lock = threading.Lock()
download_queue = queue.Queue()
file_name_ignore_list = ['/', '\\', ':', '"', '<', '>', '?', '|', '*']


class download_producer(threading.Thread):
    '''
    下载的生产者，根据匹配规则和统计共有多少歌曲生成队列
    '''

    def __init__(self, magazine_id):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_producer'
        self.magazine_id = magazine_id

    def run(self):
        download_lock.acquire()
        tmp = spider4id(magazine_id=self.magazine_id)
        soup = tmp.spider()
        if soup.find('div', {'class': 'error-msg'}):
            return
        else:
            pass

        music_player_node = soup.find(
            'div', {'id': 'luooPlayerPlaylist'}).find('ul').find_all('li')
        song_list = len(music_player_node) + 1

        for i in range(1, song_list):
            if len(str(i)) == 1:
                i = '0%s' % i
            base_url = mp3url(magazine_id=self.magazine_id)
            download_url = '%s%s.mp3' % (base_url, i)
            download_queue.put(download_url)
            pass



class download_consumer(threading.Thread):
    '''
    下载的消费者，从队列中取出相应的url下载
    '''

    def __init__(self, magazine_id):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_consumer'
        self.save_path = magazine_id

    def run(self):
        for i in range(download_queue.qsize()):
            song_url = download_queue.get(block=False)
            s = requests.Session()
            s.mount(prefix=song_url, adapter=HTTPAdapter(max_retries=5))
            r = s.get(url=song_url)

            if r.status_code != 200:
                logging.warning(
                    'this music cant download -> {}'.format(song_url))
                pass

            song_name = song_url.split('/')[-1]

            if os.path.exists('{}/{}'.format(self.save_path, song_name)):
                continue

            with open('{}/{}'.format(self.save_path, song_name), 'wb') as song:
                song.write(r.content)

            logging.info('{}/{} downloaded'.format(self.save_path, song_name))

            # 使用mutagen读取id3信息，更改歌曲名
            file = MP3('%s/%s' % (self.save_path, song_name))
            artist = str(
                file['TPE1']).encode(
                encoding='latin1').decode('gb18030')
            music_name = str(
                file['TIT2']).encode(
                encoding='latin1').decode('gb18030')

            # 在Windows平台中，文件名不能包括某些字符
            if 'Windows' in platform.system():
                for i in file_name_ignore_list:
                    music_name = music_name.replace(i, '')
                    artist = artist.replace(i, '')
                    pass
                pass
            try:
                os.rename('{}/{}'.format(self.save_path,song_name),
                          '{}/{}'.format(self.save_path,
                                         '{}-{}.mp3'.format(artist,music_name)))
                pass

            except Exception as e:
                os.remove('%s/%s' % (self.save_path, song_name))
                pass
