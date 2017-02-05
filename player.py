import os
import pyglet
# need AVbin10 to play music


def play_music(folder):
    # 判断是否存在路径
    if os.path.exists(folder) is not True:
        return

    def player(music_path):
        print(music_path)
        play = pyglet.media.load(music)
        play.play()
        pyglet.app.run()


    # 遍历路径中的音乐，循环播放
    for music in os.listdir(folder):
        music = '%s/%s' % (folder, music)
        player(music_path=music)

def main(magazine_id):
    play_music(folder=str(magazine_id))


if __name__ == '__main__':
    main(magazine_id='886')