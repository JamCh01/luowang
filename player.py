import pyglet
import logging
import datetime


# need AVbin10 to play music
# you can download it from here -> http://avbin.github.io/AVbin/Download.html


class music_player(object):
    '''
    播放器类，播放音乐
    '''

    def __init__(self, music_list):
        self.music_list = music_list

    @staticmethod
    def __exiter(dt):
        pyglet.app.exit()

    def play(self):
        '''
        播放器
        :return:
        '''
        start_time = datetime.datetime.now()
        # 遍历音乐列表中的音乐，循环播放
        for music in self.music_list:
            try:
                # 加载音乐
                player = pyglet.media.load(music)
            except Exception as e:
                logging.error(
                    msg='需要使用AVbin支持播放，下载地址->http://avbin.github.io/AVbin/Download.html')
                return
            play_time = player.duration
            print('''正在播放‘{}’，总时长：{}s'''.format(music, str(play_time)))
            # 播放音乐
            player.play()
            # 设置延时任务，时间为正在播放的音乐时长，任务为退出pyglet（__exiter）
            pyglet.clock.schedule_once(self.__exiter, play_time)
            # 启动pyglet
            pyglet.app.run()
            pass

        end_time = datetime.datetime.now()
        minute = (end_time - start_time).seconds // 60
        second = (end_time - start_time).seconds % 60
        print('播放结束，总共耗时{}min {}s，再会'.format(str(minute), str(second)))
        return