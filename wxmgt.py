#!/usr/bin/env python
# coding: utf-8
import sys
import logging
import random
from weixin import WebWeixin
from wxrobot import WxRobot


def catchKeyboardInterrupt(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except KeyboardInterrupt:
            print('\n[*] 强制退出程序')
            logging.debug('[*] 强制退出程序')
    return wrapper

@catchKeyboardInterrupt
def wx_start():
    wxrobot = WxRobot()
    webwxs = []
    try:
        with open('wxrobots.txt', 'r') as f:
            for line in f.readlines():  # 依次读取每行
                line = line.strip()  # 去掉每行头尾空白
                if not len(line) or line.startswith('#'):  # 判断是否是空行或注释行
                    continue  # 是的话，跳过不处理
                webwx = WebWeixin(line)
                webwx.DEBUG = True
                webwx.TimeOut = 30
                webwx.start2(wxrobot)
                webwxs.append(webwx)
            f.close()
    except:
        pass

    if len(webwxs) == 0:
        deviceId = 'e' + repr(random.random())[2:17]
        webwx = WebWeixin(deviceId)
        webwx.DEBUG = True
        webwx.TimeOut = 30
        webwx.start2(wxrobot)
        webwxs.append(webwx)
        try:
            with open('wxrobots.txt', 'w') as f:
                f.write(deviceId)
                f.close()
        except:
            pass


    while True:
        text = input('')
        if text == 'quit':
            webwx.stop2()
            exit()

class UnicodeStreamFilter:

    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding

    def write(self, s):
        if type(s) == str:
            s = s.decode('utf-8')
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

    def flush(self):
        self.target.flush()

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if not sys.platform.startswith('win'):
        import coloredlogs
        coloredlogs.install(level='DEBUG')

    wx_start()