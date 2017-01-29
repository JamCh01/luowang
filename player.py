import os
import config
download_folder = config.download_folder

def play_music(folder):
    if os.path.exists(folder) is not True:
        return

    for music in os.listdir(folder):
        print(music)


play_music(folder='886')