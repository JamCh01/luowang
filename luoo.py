import requests
from bs4 import BeautifulSoup

class common(object):
    '''
    基础页面爬虫
    '''
    def __init__(self):
        self.headers = {
            'Host':
                'www.luoo.net',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.url = ''
    def spider(self):
        r = requests.get(url=self.url, headers=self.headers)
        res = (r.text.encode(r.encoding).decode('utf8'))
        soup = BeautifulSoup(res, 'html.parser')
        return soup

class spider4id(common):

    def __init__(self, magazine_id):
        common.__init__(self)
        self.headers['Referer'] = 'http://www.luoo.net/music/'
        self.magazine_id = magazine_id
        self.url = 'http://www.luoo.net/music/%s' % magazine_id


def mp3url(magazine_id):
    # 落网匹配规则
    base_url = 'http://mp3-cdn.luoo.net/low'
    magazine_id = int(magazine_id)
    if magazine_id == 497:
        return '%s/luoo/s1/' % (base_url)

    elif magazine_id >= 498 and magazine_id <= 521:
        return '%s/luoo/S%s/' % (base_url, str(magazine_id - 496))

    elif magazine_id == 522:
        return '%s/luoo/s26/'

    elif magazine_id >= 523 and magazine_id <= 539:
        return '%s/anbai/radio%s/' % (base_url, str(magazine_id - 522))

    elif magazine_id >= 540 and magazine_id <= 543:
        return '%s/china/radio%s/' % (base_url, str(magazine_id - 539))

    elif magazine_id == 545:
        return '%s/china/radio5/' % (base_url)

    elif magazine_id >= 546 and magazine_id <= 557:
        return '%s/world/radio%s/' % (base_url, str(magazine_id - 545))

    elif magazine_id == 558 or magazine_id == 559:
        return '%s/electric/radio%s/' % (base_url, str(magazine_id - 557))

    elif magazine_id == 560 or magazine_id == 561:
        return '%s/classical/radio%s/' % (base_url, str(magazine_id - 559))

    elif magazine_id >= 562 and magazine_id <= 565:
        return '%s/jazz/radio%s/' % (base_url, str(magazine_id - 561))

    elif magazine_id == 569:
        return '%s/electric/radio3/' % (base_url)

    elif magazine_id == 573:
        return '%s/luoo/radio499/' % (base_url)

    elif magazine_id == 576:
        return '%s/jazz/radio5/' % (base_url)

    elif magazine_id == 581:
        return '%s/luoo/radio500/' % (base_url)

    elif magazine_id == 582:
        return '%s/luoo/radio581/' % (base_url)

    elif magazine_id == 583:
        return '%s/anbai/radio18/' % (base_url)

    elif magazine_id == 594:
        return '%s/anbai/radio19/' % (base_url)

    else:
        return '%s/luoo/radio%s/' % (base_url, magazine_id)


