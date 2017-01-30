import os
import queue
import config
import requests
import threading
from mutagen.mp3 import MP3
from luoo import spider4id
from luoo import mp3url

download_queue = queue.Queue()
download_lock = threading.Lock()


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


class download_consumer(threading.Thread):
    '''
    下载的消费者，从队列中取出相应的url下载
    '''

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_consumer'

    def run(self):
        download_lock.release()
        while True:
            try:
                song_url = download_queue.get()
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
                new_name = str(
                    file['TIT2']).encode(
                    encoding='latin1').decode('gb18030')
                try:
                    os.rename(
                        '%s/%s' %
                        (save_path, song_name), '%s/%s' %
                        (save_path, '%s-%s.mp3' %
                         (artist, new_name)))
                except Exception as e:
                    os.remove('%s/%s' % (save_path, song_name))
            except Exception as e:
                break


def main(magazine_id):
    test = download_producer(magazine_id=magazine_id)
    test.start()
    test.join()
    test_ = download_consumer()
    test_.start()
    test_.join()

if __name__ == '__main__':
    magazine_id = 886
    save_path = magazine_id
    if os.path.exists(str(save_path)):
        pass
    else:
        os.makedirs(str(save_path))

    main(magazine_id=magazine_id)
