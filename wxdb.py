#!/usr/bin/env python
# coding: utf-8
import sys
import socket
import logging
import json
import psycopg2
import psycopg2.extras
import psycopg2.pool


class WxDb(object):
    def __init__(self):
        self.pool = self._createpool()

    def getRobots(self):
        pass

    def getUnstartedWxRobot(self):
        sql = 'select * from robot_wx_hosting t ' \
              'where t.status=1 and (t.device_server is null or t.device_server=\'%s\') ' \
              'order by t.device_server desc, t.priority desc;' % (self._getLocalServer())
        return self._dbFetchAll(sql)

    def loadWxConfig(self, webwx, config):
        if config and webwx.uin == '' and not config.get('wx_uin') == '':
            webwx.uin = config.get('wx_uin')
        data = self._loadWxLastSync(webwx.deviceId, webwx.uin)
        if data:
            webwx.uin = data["uin"]
            webwx.sid = data["sid"]
            webwx.skey = data["skey"]
            webwx.pass_ticket = data["pass_ticket"]
            webwx.base_uri = data["base_uri"]
            webwx.uuid = data["uuid"]
            webwx.synckey = data["synckey"]
            webwx.SyncKey = json.loads(data["jsonsync"])

    def saveWxConfig(self, webwx, config=None):

        ## check hosting
        sql = ''
        if config:
            sql = 'select * from robot_wx_hosting ' \
                  'where device_id=\'%s\' and (wx_uin is null or wx_uin=\'\' or wx_uin=\'%s\'); ' \
                  % (webwx.deviceId, webwx.uin)
        else:
            sql = 'select * from robot_wx_hosting ' \
                  'where device_id=\'%s\' and uin=\'%s\' ;' \
                  % (webwx.deviceId, webwx.uin)
        data = self._dbFetchOne(sql)
        if data:
            sql = 'update robot_wx_hosting ' \
                  'set device_id=\'%s\', wx_uin=\'%s\', device_server=\'%s\', wx_name=\'%s\', updated_time=current_timestamp ' \
                  'where id=%s; ' \
                  % (webwx.deviceId, webwx.uin, self._getLocalServer(), webwx.User['NickName'], data['id'])
        else:
            remarks = ''
            sql = 'insert into robot_wx_hosting(account, type, device_server, device_id, wx_uin, wx_name' \
                  ', status, created_time, updated_time, remarks) ' \
                  'values(\'temp\',\'temp\',\'%s\', \'%s\', \'%s\', \'%s\', 1, current_timestamp, current_timestamp, \'%s\'); ' \
                  % (self._getLocalServer(), webwx.deviceId, webwx.uin, webwx.User['NickName'], remarks)
        self._dbExecuteSql(sql)

        self.updateWxSync(webwx)

    def loadLivingConfig(self, uin=None):
        sql = "select * from robot_wx_living" \
              " where (hosting_uin is null or hosting_uin='%s') and status=1" \
              " order by living_num, living_type; " % (uin)
        return self._dbFetchAll(sql)

    def updateWxUser(self, webwx, ignorCheck=False):
        pass

    def _loadWxLastSync(self, device_id, uin):
        sql = 'select * from wx_synckey t ' \
              'where t.device_id=\'%s\' and t.uin=\'%s\' ' \
              'order by t.updated_time desc limit 1;' % (device_id, uin)
        return self._dbFetchOne(sql)

    def updateWxSync(self, webwx, ignorCheck=False):
        if ignorCheck:
            sql = 'update wx_synckey set synckey=\'%s\', jsonsync=\'%s\', updated_time=current_timestamp ' \
                  'where device_id=\'%s\' and uin=\'%s\' and sid=\'%s\' and skey=\'%s\' and pass_ticket=\'%s\' ;' \
                  % (webwx.synckey, json.dumps(webwx.SyncKey), webwx.deviceId, webwx.uin, webwx.sid, webwx.skey,
                     webwx.pass_ticket)
            return self._dbExecuteSql(sql)

        sql = 'select * from wx_synckey t ' \
              ' where t.device_id=\'%s\' and t.uin=\'%s\' and t.sid=\'%s\' and t.skey=\'%s\' and t.pass_ticket=\'%s\' ' \
              ' order by t.updated_time desc limit 1;' \
              % (webwx.deviceId, webwx.uin, webwx.sid, webwx.skey, webwx.pass_ticket)
        record = self._dbFetchAll(sql)
        if record:
            sql = 'update wx_synckey set synckey=\'%s\', jsonsync=\'%s\', updated_time=current_timestamp ' \
                  'where device_id=\'%s\' and uin=\'%s\' and sid=\'%s\' and skey=\'%s\' and pass_ticket=\'%s\' ' \
                  % (webwx.deviceId, webwx.uin, webwx.sid, webwx.skey, webwx.pass_ticket)
        else:
            sql = 'insert into wx_synckey(device_id, uin, sid, skey, pass_ticket, uuid, base_uri, username' \
                  ', synckey, jsonsync, created_time, updated_time) ' \
                  ' values( \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', current_timestamp, current_timestamp ); ' \
                  % (webwx.deviceId, webwx.uin, webwx.sid, webwx.skey, webwx.pass_ticket
                     , webwx.uuid, webwx.base_uri, webwx.User['UserName'], webwx.synckey, json.dumps(webwx.SyncKey))
        return self._dbExecuteSql(sql)

    def saveWxMsg(self, uin, msgid, msg):
        sql = 'insert into wx_msg(uin, msgid, jsonmsg, updated_time) values(%s,%s,%s, current_timestamp);'
        self._dbExecuteSql(sql, (uin, msgid, json.dumps(msg, indent=4, ensure_ascii=False)))
        pass

    def saveWxChat(self, chat):
        sql = 'insert into robot_wx_chat(wx_uin, type, msg_id, refer_id' \
              ', from_id, from_name, to_id, to_name, room_id, room_name' \
              ', msg_type, msg_content, msg_file, msg_other, updated_time) ' \
              'values(%s, %s, %s, %s' \
              ', %s, %s, %s, %s, %s, %s' \
              ', %s, %s, %s, %s, current_timestamp);'
        self._dbExecuteSql(sql, (chat['uin'], chat['type'], chat['msg_id'], chat['refer_id']
                                 , chat['from_id'], chat['from_name'], chat['to_id'], chat['to_name'], chat['room_id'],
                                 chat['room_name']
                                 , chat['msg_type'], chat['msg_content'], chat['msg_file'], chat['msg_other']))
        pass

    def _getLocalServer(self):
        serverName = socket.gethostname()
        if not serverName:
            serverName = 'wxrobotserver'
        return serverName

    def _dbFetchAll(self, sql):
        conn = None
        try:
            conn = self.pool.getconn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            return rows
        except Exception as e:
            print(e)
        finally:
            if conn:
                self.pool.putconn(conn)
        return

    def _dbFetchOne(self, sql):
        conn = None
        try:
            conn = self.pool.getconn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql)
            data = cur.fetchone()
            conn.commit()
            cur.close()
            return data
        except Exception as e:
            print(e)
        finally:
            if conn:
                self.pool.putconn(conn)
        return

    def _dbExecuteSql(self, sql, args=None):
        try:
            conn = self.pool.getconn()
            cur = conn.cursor()
            if args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)
            conn.commit()
            cur.close()
            self.pool.putconn(conn)
        except Exception as e:
            print(e)
            if conn:
                self.pool.putconn(conn)
        finally:
            pass

        return

    def _getconn(self):
        return self.pool.getconn()

    def _createpool(self):
        pool = psycopg2.pool.ThreadedConnectionPool(2, 10, database='postgres', user='postgres', password='open2018',
                                                    host='112.124.35.123', port='5701')
        return pool


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if not sys.platform.startswith('win'):
        import coloredlogs

        coloredlogs.install(level='DEBUG')

    wxdb = WxDb()
    wxdb.getUnstartedWxRobot()
