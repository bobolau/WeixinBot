#!/usr/bin/env python
# coding: utf-8
import logging
import re
import os
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import requests
import copy


class WxRobot(object):

    def __init__(self):
        self.re_command = re.compile(r'#(.{2,12})#')
        self.re_emoji = re.compile(r'<span class="emoji emoji([0-9a-zA-Z]{2,10})"></span>')
        self.saveFolder = os.path.join(os.getcwd(), 'saved')

    def loadWxConfig(self, webwx, config=None):
        if not webwx:
            return

        # for test only
        # if config:
        #     try:
        #         with open(self._getfile_wxconfig(webwx.deviceId), 'r') as f:
        #             data = json.loads(f.read())
        #             pass
        #     except:
        #         pass

        if config and config["lastlogin"]:
            #webwx.deviceId = data["lastlogin"]["deviceId"]
            webwx.uin = config["lastlogin"]["uin"]
            webwx.sid = config["lastlogin"]["sid"]
            webwx.skey = config["lastlogin"]["skey"]
            webwx.pass_ticket = config["lastlogin"]["pass_ticket"]
            webwx.base_uri = config["lastlogin"]["base_uri"]
            webwx.uuid = config["lastlogin"]["uuid"]
        else:
            try:
                with open(self._getfile_wxdump(webwx.deviceId), 'r') as f:
                    webwx.__dict__.update(json.loads(f.read()))
                    pass
            except:
                pass


        if webwx.cookie:
            webwx.cookie.load(self._getfile_wxcookie(webwx.deviceId),ignore_expires=True,ignore_discard=True)
            pass



    def saveWxConfig(self, webwx):
        if not webwx:
            return

        config = r'{"lastlogin":{"uin":"%s","sid":"%s","skey":"%s","pass_ticket":"%s","deviceId":"%s","base_uri":"%s","uuid":"%s"}}' %(
                webwx.uin, webwx.sid, webwx.skey, webwx.pass_ticket, webwx.deviceId, webwx.base_uri, webwx.uuid)
        with open(self._getfile_wxconfig(webwx.deviceId), 'w') as f:
            f.write(config)
            f.close()

        if webwx.cookie:
            webwx.cookie.save(self._getfile_wxcookie(webwx.deviceId),ignore_expires=True,ignore_discard=True)
            pass

        with open(self._getfile_wxdump(webwx.deviceId), 'w') as f:
            webwx2 = copy.copy(webwx)
            webwx2.cookie = None
            webwx2.wxRobot = None
            webwx2.__dict__.pop('wxRobot')
            webwx2.__dict__.pop('cookie')
            json_str = json.dumps(webwx2.__dict__)
            f.write(json_str)
            f.close()

    def _getfile_wxdump(self, deviceId):
        return os.path.join(self.saveFolder, deviceId + '_dump.txt')

    def _getfile_wxconfig(self, deviceId):
        return os.path.join(self.saveFolder, deviceId + '_config.txt')

    def _getfile_wxcookie(self, deviceId):
        return os.path.join(self.saveFolder, deviceId + '_cookie.txt')

    def handleWxMsg(self, webwx, msg):
        msgType = msg['MsgType']
        fromUser = msg['FromUserName']
        srcName = webwx.getUserRemarkName(msg['FromUserName'])
        dstName = webwx.getUserRemarkName(msg['ToUserName'])
        content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
        msgid = msg['MsgId']

        # verify user
        if msgType == 37:
            # 好友推荐，自动加为好友
            toUser = msg['RecommendInfo']['UserName']
            ticket = msg['RecommendInfo']['Ticket']
            webwx.webwxverifyuser(toUser, ticket)
            return

        # system message
        if msgType == 10000:
            if fromUser[:2] == '@@':
                regx = '"(\S+?)"邀请"(\S+?)"加入了群聊'
                pm = re.search(regx, content)
                if pm:
                    person1 = pm.group(1)
                    person2 = pm.group(2)
                    replyContent = '欢迎%s(%s好友)加入 @%s' % (person2, person1, person2)
                    webwx.webwxsendmsg(replyContent, fromUser)
            return

        if msgType == 10002:
            if fromUser[:2] == '@@':
                pass
            else:
                pass
            return

        # check command like "#command# ......"
        if msgType == 1 and self.re_command.match(content):
            command = self.re_command.search(content).group(0)
            logging.debug('[*] 接到命令：' + command + '，cotent=' + content)
            return


        # auto reply message (robot)
        if msgType == 1:
            if not fromUser[:2] == '@@':
                replyContent = self.talk2Robot(content, fromUser)
                if webwx.webwxsendmsg(replyContent, fromUser):
                    logging.info('自动回复: ' + replyContent)
                else:
                    logging.info('自动回复失败')
            else:
                if ":<br/>" in content:
                    [people, content] = content.split(':<br/>', 1)
                    srcName = webwx.getUserRemarkName(people)
                    if content.startswith('@' + dstName):
                        content = content[(len(dstName) + 2):]
                        replyContent = '@' + srcName + '  ' + self.talk2Robot(content, srcName)
                        if webwx.webwxsendmsg(replyContent, fromUser):
                            logging.info('自动回复: ' + replyContent)
                        else:
                            logging.info('自动回复失败')
        # group living
        if fromUser[:2] == '@@':
            self.process_group_living(webwx, msg)



    def process_command(self, webwx, msg, command):
        # 群命令
        if msg['FromUserName'][:2] == '@@':
            # 群直播主群命令：申请直播|取消直播|设置主播
            # 群直播转播群命令：接收转播(直播号)|停止转播(直播号)
            # 通用群命令：参数设置
            pass
        # 好友命令
        else:
            # 主号命令：小号托管
            # 小号命令：取消托管
            pass
        return

    def process_group_living(self, webwx, msg):
        msgType = msg['MsgType']
        fromUser = msg['FromUserName']
        srcName = webwx.getUserRemarkName(msg['FromUserName'])
        content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
        msgid = msg['MsgId']
        # 3.check group live
        if fromUser[:2] == '@@' and self.group_living.has_key(srcName):
            toGroups = self.group_living.get(srcName)
            if ":<br/>" in content:
                [people, content] = content.split(':<br/>', 1)
                groupName = srcName
                srcName = webwx.getUserRemarkName(people)
                replyContent = '[转]' + groupName + '->' + srcName + ':<br/>' + content
            else:
                groupName = srcName
                replyContent = '[转]' + groupName + ':<br/>' + content
            replyContent = self.formatMsg(replyContent, groupName + '->' + srcName)
            for toGroup in re.split(r'[\s\,\;]+', toGroups):
                toGroupId = webwx.getGroupId(toGroup)
                if not toGroupId:
                    continue
                if msgType == 1:
                    if webwx.webwxsendmsg(replyContent, toGroupId):
                        logging.info('群转发: ' + replyContent)
                    else:
                        logging.info('群转发文字失败, group=' + toGroup + '(' + toGroupId + ')')
                elif msgType == 3:
                    image = webwx.webwxgetmsgimg(msgid)
                    response = webwx.webwxuploadmedia(image)
                    media_id = ""
                    if response is not None:
                        media_id = response['MediaId']
                    if webwx.webwxsendmsgimg(toGroupId, media_id):
                        logging.info('群转发图片成功')
                    else:
                        logging.info('群转发图片失败')
            return


    def talk2Robot(self, info, userid, myid='robot'):
        reply = self.robot_tuling(info, userid)
        return reply.decode('utf-8')

    def robot_tuling(self, info, userid):
        key = 'ec15bb3e9e524e46868bc3b7c5a9cde3'
        url = 'http://www.tuling123.com/openapi/api?key=%s&info=%s&userid=%s' % (key, info, userid)
        r = requests.get(url)
        ans = r.json()
        # code, text, url
        if ans['code'] == '100000':
            return ans['text'].encode('utf-8')
        if ans['code'] == '200000':
            return ans['text'].encode('utf-8') + ans['url']
        return ans['text'].encode('utf-8')

    def robot_xiaodoubi(self, word):
        url = 'http://www.xiaodoubi.com/bot/chat.php'
        try:
            r = requests.post(url, data={'chat': word})
            return r.content
        except:
            return "让我一个人静静 T_T..."

    def robot_simsimi(self, word):
        key = ''
        url = 'http://sandbox.api.simsimi.com/request.p?key=%s&lc=ch&ft=0.0&text=%s' % (
            key, word)
        r = requests.get(url)
        ans = r.json()
        if ans['result'] == '100':
            return ans['response']
        else:
            return '你在说什么，风太大听不清列'