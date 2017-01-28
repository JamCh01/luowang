import os
import config
import pyglet

download_folder = config.download_folder

def play_music(folder):
    if os.path.exists(folder) is not True:
        return

    for music in os.listdir(folder):
        music = r'%s\%s\%s'% (os.getcwd(), folder, music)
        a = pyglet.media.load(music)
        a.play()
play_music(folder='886')