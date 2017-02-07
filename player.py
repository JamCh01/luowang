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
        '''
        播放器
        :return:
        '''
        # 遍历音乐列表中的音乐，循环播放
        for music in self.music_list:
            # 加载音乐
            player = pyglet.media.load(music)
            print('''正在播放‘{}’，总时长：{}s'''.format(music, str(player.duration)))
            # 播放音乐
            player.play()
            # 设置延时任务，时间为正在播放的音乐时长，任务为退出pyglet（__exiter）
            pyglet.clock.schedule_once(self.__exiter, player.duration)
            # 启动pyglet
            pyglet.app.run()
    def favorite(self):
        print('播放结束，请选择其中的歌曲编号加入喜欢列表（若无喜爱请输入pass）')
        for music in enumerate(self.music_list):
            print('编号:{}, 歌曲名:{}'.format(music[0], music[1]))
        while True:
            if input('->') == 'pass':
                return
            elif input('->') in range(len(self.music_list)):
                pass
            else:
                print('->喵喵喵？')



def run_player(folder):
    folder = str(folder)
    if os.path.exists(folder) is not True:
        return
    # 拼接歌曲存储地址
    player = music_player(
        music_list=[
            '%s/%s' %
            (folder, i) for i in os.listdir(folder)])
    player.play()

def run_player_with_favorite(folder):
    folder = str(folder)
    if os.path.exists(folder) is not True:
        return
    # 拼接歌曲存储地址
    player = music_player(
        music_list=[
            '%s/%s' %
            (folder, i) for i in os.listdir(folder)])
    player.play()
    player.favorite()

# todo 完成列表循环；加入一个SQLite，作为路径存储和播放列表
