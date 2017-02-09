import os
import orm
import sys
import queue
import platform
import requests
import threading
from mutagen.mp3 import MP3
from luoo import spider4id
from luoo import mp3url
from player import run_player

download_queue = queue.Queue()
download_lock = threading.Lock()
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
        try:
            magazine_name = soup.find('title').text.strip().replace('-落网', '')
        except Exception as e:
            magazine_name = 'UNKNOW'

        try:
            magazine_tag = soup.find(
                'a', {'class': 'vol-tag-item'}).text.strip().replace('#', '')
        except Exception as e:
            magazine_tag = 'UNKNOW'

        if check.check_magazine(magazine_id=magazine_id):
            return
        magazine_session = orm.DBSession()
        magazine = orm.magazine(
            magazine_id=self.magazine_id,
            magazine_name=magazine_name,
            magazine_tag=magazine_tag,
            magazine_total=str(
                len(music_player_node)))
        magazine_session.add(magazine)
        magazine_session.commit()
        magazine_session.close()


class download_consumer(threading.Thread):
    '''
    下载的消费者，从队列中取出相应的url下载
    '''

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_consumer'

    def run(self):
        for i in range(download_queue.qsize()):
            song_url = download_queue.get(block=False)
            r = requests.get(url=song_url, stream=True)
            if r.status_code != 200:
                with open('error.txt', 'w') as error:
                    error.write('download_file %s' % song_url + '\n')
                error.close()
                continue
            song_name = song_url.split('/')[-1]
            if os.path.exists('%s/%s' % (save_path, song_name)):
                continue
            with open('%s/%s' % (save_path, song_name), 'wb') as song:
                song.write(r.content)

            print('%s/%s' % (save_path, song_name))
            # 使用mutagen读取id3信息，更改歌曲名
            file = MP3('%s/%s' % (save_path, song_name))
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
            try:
                os.rename(
                    '%s/%s' %
                    (save_path, song_name), '%s/%s' %
                    (save_path, '%s-%s.mp3' %
                     (artist, music_name)))
            except Exception as e:
                os.remove('%s/%s' % (save_path, song_name))
            song_name = '%s-%s.mp3' % (artist, music_name)

            if check.check_music(
                    magazine_id=magazine_id,
                    music_name=song_name):
                return
            download_session = orm.DBSession()
            music_info = orm.music(
                music_name=song_name,
                magazine_id=magazine_id,
                music_artist=artist,
                music_save_path=magazine_id)
            download_session.add(music_info)
            download_session.commit()
            download_session.close()


def main(magazine_id):
    producer = download_producer(magazine_id=magazine_id)
    producer.start()
    producer.join()
    # 判断下载目录中是否存在与下载队列相同的文件数目（目前以这种方法判断了……）
    if download_queue.qsize() != len(os.listdir(path=magazine_id)):
        for i in range(int(download_queue.qsize())):
            consumer = download_consumer()
            consumer.start()
            consumer.join()

    run_player(folder=magazine_id)


if __name__ == '__main__':
    magazine_id = sys.argv[1]
    save_path = magazine_id
    if os.path.exists(str(save_path)):
        pass
    else:
        os.makedirs(str(save_path))
    check = orm.check()
    main(magazine_id=magazine_id)
