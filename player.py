import os
import pyglet
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
        # 遍历音乐列表中的音乐，循环播放
        for music in self.music_list:
            # 加载音乐
            player = pyglet.media.load(music)
            print('''正在播放‘{}’，总时长：{}s'''.format(music,str(player.duration)))
            # 播放音乐
            player.play()
            # 设置延时任务，时间为正在播放的音乐时长，任务为退出pyglet
            pyglet.clock.schedule_once(self.__exiter, player.duration)
            # 启动pyglet
            pyglet.app.run()



def main(magazine_id):
    magazine_id = str(magazine_id)
    if os.path.exists(magazine_id) is not True:
        return

    player = music_player(music_list=['%s/%s' % (magazine_id, i) for i in  os.listdir(magazine_id)])
    player.play()


if __name__ == '__main__':
    main(magazine_id='886')
    # todo 整理代码；完成列表循环；加入一个SQLite，作为路径存储和播放列表