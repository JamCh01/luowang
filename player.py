import os
import orm
import shutil
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
        if os.path.exists('favorite'):
            pass
        else:
            os.makedirs('favorite')

        print('本期期刊播放结束，请选择其中的歌曲编号加入喜欢列表（若无喜爱请输入pass）')
        for music in enumerate(self.music_list):
            music_name = music[1].split('/', 1)[1]
            print('编号:{}, 歌曲名:{}'.format(music[0], music_name))
        while True:
            tmp = input('->')
            print(len(self.music_list))
            print(self.music_list[0])
            if tmp == 'pass':
                break
            elif tmp in range(len(self.music_list)):
                try:
                    favorite_session = orm.DBSession()
                    magazine_id = self.music_list[tmp].split('/', 1)[0]
                    music_name = self.music_list[tmp].split('/', 1)[1]
                    music_artist = music_name.split('-', 1)[0]
                    music_save_path = self.music_list[tmp]
                    favorite_music = orm.music(
                        music_name=music_name,
                        magazine_id=magazine_id,
                        music_artist=music_artist,
                        music_save_path=music_save_path)
                    favorite_session.add(favorite_music)
                    favorite_session.commit()
                    favorite_session.close()
                except Exception as e:
                    print('->好像没有诶')
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
