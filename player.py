import os
import orm
import time
import shutil
import pyglet
import datetime

# need AVbin10 to play music
# you can download it from here -> http://avbin.github.io/AVbin/Download.html


class music_player(object):
    '''
    播放器类，播放音乐
    '''

    def __init__(self, folder, music_list):
        self.music_list = music_list
        self.folder = folder
        self.check = orm.check()

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
            try:
                # 加载音乐
                player = pyglet.media.load(music)
            except Exception as e:
                print('需要使用AVbin支持播放，下载地址->http://avbin.github.io/AVbin/Download.html')
            play_time = player.duration
            music_info_session = orm.DBSession()
            music_info_session.query(orm.music).filter_by(
                music_name=music.split('/')[1]).update({'play_time': int(play_time)})
            music_info_session.flush()
            music_info_session.commit()
            music_info_session.close()

            print('''正在播放‘{}’，总时长：{}s'''.format(music, str(play_time)))
            # 播放音乐
            player.play()
            # 设置延时任务，时间为正在播放的音乐时长，任务为退出pyglet（__exiter）
            pyglet.clock.schedule_once(self.__exiter, play_time)
            # 启动pyglet
            pyglet.app.run()

        if self.folder == 'favorite':
            pass
        else:
            if self.check.check_new(magazine_id=self.folder) == 1:
                # self.favorite()
                player_session = orm.DBSession()
                player_session.query(orm.magazine.new).filter_by(
                    magazine_id=self.folder).update({'new': 0})
                player_session.flush()
                player_session.commit()
                player_session.close()
        self.favorite_show()
        self.favorite_add()

    def favorite(self):
        if os.path.exists('favorite'):
            pass
        else:
            os.makedirs('favorite')

    def favorite_add(self):
        self.favorite()
        print('本期期刊播放结束，请选择其中的歌曲编号加入喜欢列表（若无喜爱请输入pass）')
        for music in enumerate(self.music_list):
            music_name = music[1].split('/', 1)[1]
            print('编号:{}, 歌曲名:{}'.format(music[0], music_name))
        while True:
            tmp = input('->')
            if tmp == 'pass':
                break
            elif int(tmp) in range(0, len(self.music_list)):
                tmp = int(tmp)
                try:
                    favorite_session = orm.DBSession()
                    magazine_id = self.music_list[tmp].split('/', 1)[0]
                    music_name = self.music_list[tmp].split('/', 1)[1]
                    music_artist = music_name.split('-', 1)[0]
                    music_save_path = self.music_list[tmp]
                    if self.check.check_favorite(
                            magazine_id=magazine_id, music_name=music_name):
                        print('->这首歌已经在喜欢列表啦╭(′▽`)╭(′▽`)╯')
                        continue
                    favorite_music = orm.favorite(
                        music_name=music_name,
                        magazine_id=magazine_id,
                        music_artist=music_artist,
                        music_save_path=music_save_path,
                        add_time=datetime.datetime.now(),
                        play_time=favorite_session.query(
                            orm.music.play_time).filter_by(
                            music_name=music_name)[0][0])
                    favorite_session.add(favorite_music)
                    favorite_session.commit()
                    favorite_session.close()
                except Exception as e:
                    print(e)
                    print('->好像没有诶')

            else:
                print('->喵喵喵？')

    def favorite_delete(self):
        # todo 删除
        self.favorite()

    def favorite_show(self):
        #todo 展示
        show_session = orm.DBSession()
        show_session.query(orm.favorite).all()



def run_player(folder):
    folder = str(folder)
    if os.path.exists(folder) is not True:
        return
    # 拼接歌曲存储地址
    player = music_player(folder=folder,
                          music_list=[
                              '%s/%s' %
                              (folder, i) for i in os.listdir(folder)])
    player.play()

# todo 完成列表循环；加入一个SQLite，作为路径存储和播放列表
