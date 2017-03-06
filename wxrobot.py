#!/usr/bin/env python
# coding: utf-8
import logging
import re
import os
import json
import random
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import requests
import copy
from weixin import WebWeixin
from wxdb import WxDb


class WxRobot(object):

    def __init__(self, wxdb=None):
        self.wxdb = wxdb
        self.re_command = re.compile(r'#(.{2,12})#')
        self.re_emoji = re.compile(r'<span class="emoji emoji([0-9a-zA-Z]{2,10})"></span>')
        self.saveFolder = os.path.join(os.getcwd(), 'saved')


    def loadWxConfig(self, webwx, config=None):
        if not webwx:
            return

        ## load local first
        try:
            with open(self._getfile_wxdump(webwx.deviceId), 'r') as f:
                webwx.__dict__.update(json.loads(f.read()))
            if webwx.cookie:
                webwx.cookie.load(self._getfile_wxcookie(webwx.deviceId), ignore_expires=True, ignore_discard=True)
        except:
            pass

        if config and self.wxdb.loadWxConfig:
            self.wxdb.loadWxConfig(webwx, config)

    def saveWxConfig(self, webwx, config=None):
        if not webwx:
            return

        if  self.wxdb and self.wxdb.saveWxConfig:
            self.wxdb.saveWxConfig(webwx, config)

        ## for local only
        with open(self._getfile_wxdump(webwx.deviceId), 'w') as f:
            webwx2 = copy.copy(webwx)
            webwx2.cookie = None
            webwx2.wxRobot = None
            webwx2.__dict__.pop('wxRobot')
            webwx2.__dict__.pop('cookie')
            json_str = json.dumps(webwx2.__dict__)
            f.write(json_str)
            f.close()

        if webwx.cookie:
            webwx.cookie.save(self._getfile_wxcookie(webwx.deviceId),ignore_expires=True,ignore_discard=True)
            pass

    def updateWxSync(self, webwx, ignorCheck=False):
        if self.wxdb and self.wxdb.updateWxSync:
            self.wxdb.updateWxSync(webwx, ignorCheck)

    def _getfile_wxdump(self, deviceId):
        return os.path.join(self.saveFolder, deviceId + '_dump.txt')

    def _getfile_wxcookie(self, deviceId):
        return os.path.join(self.saveFolder, deviceId + '_cookie.txt')

    def handleWxOriginMsg(self, webwx, r, selector='2'):
        for msg in r['AddMsgList']:
            # print('[*] 你有新的消息，请注意查收')
            self.handleWxMsg(webwx, msg)
        pass

    def saveWxMsg(self, uin, msgid, msg):
        if self.wxdb and self.wxdb.saveWxMsg:
            self.wxdb.saveWxMsg(uin, msgid, msg)

    def saveWxChat(self, webwx, chat):
        if self.wxdb and self.wxdb.saveWxChat:
            if chat and 'msg_content' in chat:
                self.wxdb.saveWxChat(chat)

            if chat and 'reply_content' in chat:
                chat['type'] = '2'
                chat['refer_id'] = chat['msg_id']
                chat['msg_id'] = ''
                chat['to_id'] = chat['from_id']
                chat['to_name'] = chat['from_name']
                chat['from_id'] = webwx.User['UserName']
                chat['from_name'] = webwx.User['NickName']
                chat['msg_content'] = chat['reply_content']
                self.wxdb.saveWxChat(chat)


    def handleWxMsg(self, webwx, msg):
        msgType = msg['MsgType']
        fromUser = msg['FromUserName']
        srcName = webwx.getUserRemarkName(msg['FromUserName'])
        dstName = webwx.getUserRemarkName(msg['ToUserName'])
        content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
        msgid = msg['MsgId']

        self.saveWxMsg(webwx.uin, msgid, msg)

        chat = {}
        if self.saveWxChat:
            chat =  json.loads(json.dumps(msg))
            chat['uin'] = webwx.uin
            chat['type'] = '0'
            chat['from_id'] = fromUser
            chat['from_name'] = srcName
            chat['to_id'] = chat['ToUserName']
            chat['to_name'] = dstName
            chat['msg_type'] = msgType
            chat['msg_id'] = msgid
            chat['refer_id'] = ''
            chat['msg_content'] = content
            chat['msg_file'] = ''
            chat['msg_other'] = ''
            if fromUser[:2] == '@@':
                chat['room_id'] = fromUser
                chat['room_name'] = srcName
            else:
                chat['room_id'] = ''
                chat['room_name'] = ''

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
                    #record
                    if self.saveWxChat:
                        chat['room_id'] = fromUser
                        chat['type'] = '1'
                        self.saveWxChat(webwx, chat)
                        chat['type'] = '2'
                        chat['msg_id'] = ''
                        chat['refer_id'] = msgid
                        chat['from_id'] = chat['ToUserName']
                        chat['from_name'] = dstName
                        chat['to_id'] = fromUser
                        chat['to_name'] = srcName
                        chat['msg_content'] = replyContent
                        self.saveWxChat(webwx, chat)
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
            if self.saveWxChat:
                chat['room_id'] = fromUser
                chat['type'] = '1'
                chat['msg_other'] = command
                self.saveWxChat(webwx, chat)
            self._process_command(webwx, msg, command)
            return

        # group living
        if fromUser[:2] == '@@':
            living_num = self._get_group_living(webwx, fromUser, srcName)
            if living_num:
                self._process_group_living(webwx, msg, living_num)
                return

        # auto reply message (robot)
        if msgType == 1:
            # personal chat
            if not fromUser[:2] == '@@':
                if fromUser == webwx.User['UserName']:
                    if self.saveWxChat:
                        self.saveWxChat(webwx, chat)
                    return

                replyContent = self.talk2Robot(content, fromUser)
                if webwx.webwxsendmsg(replyContent, fromUser):
                    chat['reply_content'] = replyContent
                if self.saveWxChat:
                    self.saveWxChat(webwx, chat)
                return
            # group chat
            elif ":<br/>" in content:
                [people, content] = content.split(':<br/>', 1)
                srcName = webwx.getUserRemarkName(people)
                chat['from_id'] = people
                chat['from_name'] = srcName
                chat['to_id'] = ''
                chat['to_name'] = ''
                chat['msg_content'] = content
                if people == webwx.User['UserName']:
                    if self.saveWxChat:
                        self.saveWxChat(webwx, chat)
                    return
                if content.startswith('@' + dstName):
                    content = content[(len(dstName) + 2):]
                    chat['msg_content'] = content
                    chat['to_name'] = dstName
                    replyContent = '@' + srcName + '  ' + self.talk2Robot(content, srcName)
                    if webwx.webwxsendmsg(replyContent, fromUser):
                                #logging.info('自动回复: ' + replyContent)
                                chat['reply_content'] = replyContent
                if self.saveWxChat:
                    self.saveWxChat(webwx, chat)
                return

    def _process_command(self, webwx, msg, command):
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

    def _get_group_living(self, webwx, roomId, roomName):
        ## check and init living config
        if not hasattr(webwx, 'group_living'):
            group_living = []
            data = self.wxdb.loadLivingConfig(webwx.uin)
            if data:
                living_num = ''
                living_config = {}
                for row in data:
                    if not (living_num == row['living_num']):
                        if row['living_type'] == '1': ##直播群
                            living_num = row['living_num']
                            living_config = row.copy()
                            group_living.append(living_config)
                        else:
                            continue
                    if row['living_type']=='2':  ##转播群
                        if 'dest' not in living_config:
                            living_config['dest'] = []
                        living_config['dest'].append(row.copy())
            setattr(webwx, 'group_living', group_living)
        ## select living
        for item in getattr(webwx, 'group_living'):
            if roomId == item['room_id']:
                return item['living_num']
            if roomName == item['room_name']:  ##workaround
                item['room_id'] = roomId
                return item['living_num']
        return None

    def _process_group_living(self, webwx, msg, living_num=None):
        destGroups = []
        for item in getattr(webwx, 'group_living'):
            if living_num == item['living_num']:
                for dest in item['dest']:
                   dest_id = dest['room_id']
                   currentName = webwx.getGroupName(dest_id)
                   if currentName == '未知群':
                       dest_id = ''
                       dest_name = dest['room_name']
                       for member in webwx.GroupList:
                           if member['NickName'] == dest_name:
                               dest_id = member['UserName']
                               dest['room_id'] = dest_id  ##update room_id
                               break
                       if '' not in (dest_id):
                           destGroups.append(dest_id)

        if len(destGroups)==0:
            return

        msgType = msg['MsgType']
        content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
        fromUser = msg['FromUserName']
        srcName = webwx.getUserRemarkName(msg['FromUserName'])
        msgid = msg['MsgId']

        if ":<br/>" in content:
            [people, content] = content.split(':<br/>', 1)
            groupName = srcName
            srcName = webwx.getUserRemarkName(people)
            replyContent = '[转]' + groupName + '->' + srcName + ':<br/>' + content
        else:
            groupName = srcName
            replyContent = '[转]' + groupName + ':<br/>' + content
        ##replyContent = self.formatMsg(replyContent, groupName + '->' + srcName)
        for toGroupId in destGroups:
            if msgType == 1:
                webwx.webwxsendmsg(replyContent, toGroupId)
            elif msgType == 3:
                image = webwx.webwxgetmsgimg(msgid)
                response = webwx.webwxuploadmedia(image)
                media_id = ""
                if response is not None:
                    media_id = response['MediaId']
                webwx.webwxsendmsgimg(toGroupId, media_id)

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