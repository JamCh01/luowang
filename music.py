import os
import sys
import logging
try:
    from luoo import (download_producer,
                      download_queue,
                      download_consumer)
    from player import music_player
except FileNotFoundError:
    logging.error(msg='file not found')
    sys.exit(1)

def main(magazine_id):
    producer = download_producer(magazine_id=magazine_id)
    producer.start()
    producer.join()
    # 判断下载目录中是否存在与下载队列相同的文件数目（目前以这种方法判断了……）
    if download_queue.qsize() != len(os.listdir(path=magazine_id)):
        logging.warning(msg='downloading music…… please wait a moment')
        for i in range(int(download_queue.qsize())):
            consumer = download_consumer(magazine_id=magazine_id)
            consumer.start()
            consumer.join()
            pass
        pass

    folder = magazine_id

    if os.path.exists(folder) is not True:
        logging.warning(msg="folder {} doesn't exist".format(folder))
        return
    # 拼接歌曲存储地址
    player = music_player(music_list=[
        '{}/{}'.format(folder, i) for i in os.listdir(folder)])
    # 启动播放
    player.play()
if __name__ == '__main__':
    folder = str(sys.argv[1])
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)
    main(magazine_id=folder)
    pass