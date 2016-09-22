#-*-coding:utf-8-*-
#!/usr/bin/env python
#Created by Jam on 2016/9/19.
a = range(0,10)

def run():
    for i in a:
        yield i

for i in run():
    print i