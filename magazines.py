#-*-coding:utf-8-*-
#!/usr/bin/env python
# Created by Jam on 2016/9/13.
import os
import time
import random
import queue
import requests
import threading
from bs4 import BeautifulSoup

page_queue = queue.Queue()

class spider(object):
    def __init__(self, url):
        self.headers = {
            'Host':
                'www.luoo.net',
            'Referer':
                'http://www.luoo.net/',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.url = url
    def page_source(self):
        r = requests.get(url=self.url, headers=self.headers)
        res = (r.text.encode(r.encoding).decode('utf8'))
        soup = BeautifulSoup(res, 'html.parser')
        return soup

class page_producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'page_producer'

    def create_queue(self):
        spider4main_html = spider(url='http://www.luoo.net/tag/?p=1')
        all_num = spider4main_html.page_source().find('div', {'class': 'item'}).find('a', {'class': 'cover-wrapper'})['href'].split('/')[-1]
        print(all_num)
        return int(all_num.strip())
    def run(self):
        for i in range(self.create_queue(), 1, -1):
            print(i)
            page_queue.put(i)

class page_consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.name = 'page_consumer'

    def run(self):
        while True:
            page_id = page_queue.get()
            # print(page_id)
test_p = page_producer()
test_p.start()
test_c = page_consumer()
test_c.start()