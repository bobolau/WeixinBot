#!/usr/bin/env python
# coding: utf-8
import re

class Utils(object):
    def __init__(self):
        self.re_emoji = re.compile(r'<span class="emoji emoji([0-9a-zA-Z]{2,10})"></span>')

    def check_emoji(self, content):
        matchResult = self.re_emoji.findall(content)
        if matchResult:
            for emoji_code in matchResult:
                print 'emoji_code='+emoji_code
                if len(emoji_code) > 8:
                    emoji_str = ('\u' + emoji_code[:5]+'\u'+emoji_code[5:]).decode('unicode_escape')
                else:
                    emoji_str = ('\u' + emoji_code).decode('unicode_escape')
                content = content.replace('<span class="emoji emoji'+emoji_code+'"></span>', emoji_str)
        return content

    def test(self):
        testContent = ['xxxx<span class="emoji emoji1f1e81f1f3"></span>','<span class="emoji emoji26a1"></span><span class="emoji emoji1f44d"></span><span class="emoji emoji1f44d"></span>','xxx<span class="emoji emoji26a1"></span><span class="emoji emoji1f44d"></span>']
        for content in testContent:
            print content
            content = self.check_emoji(content)
            print content

if __name__ == '__main__':
    utils = Utils()
    utils.test()