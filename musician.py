import os
import queue
import requests
import threading
from mutagen.mp3 import MP3
from luoo import spider4musician

class download_producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_producer'

    def run(self):
        pass

class download_consumer(threading.Thread):
    '''
    下载的消费者，从队列中取出相应的url下载
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'download_consumer'

    def run(self):
        pass

