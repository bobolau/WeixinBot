#!/usr/bin/env python
# coding: utf-8
import sys
import logging
import psycopg2
import psycopg2.extras
import psycopg2.pool

class WxDb(object):
    def __init__(self):
        self.pool = self._getpool()

    def getRobots(self):
        pass



    def getUnstartedWxRobot(self):
        sql = 'select * from robot_wx_hosting h ' \
              'where h.status=1 ' \
              'order by h.priority desc;'
        return self._dbFetchAll(sql)

    def loadWxConfig(self, webwx, config):
        return
        if not webwx or not config or not config["uin"]:
            return

        webwx.uin = config["uin"]
        webwx.sid = config["sid"]
        webwx.skey = config["skey"]
        webwx.pass_ticket = config["pass_ticket"]
        webwx.base_uri = config["base_uri"]
        webwx.uuid = config["uuid"]
        webwx.synckey = config["synckey"]
        webwx.SyncKey = config["SyncKey"]

    def saveWxConfig(self, webwx):

        pass

    def loadWxSync(self, device_id, uin):
        sql = 'select * from wx_synckey t ' \
              'where t.device_id=%s and uin=%s ' \
              'order by t.updated_time desc limit 1;' % (device_id, uin)
        pass


    def saveWxChat(self):
        pass

    def _dbFetchAll(self, sql):
        conn = self._conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def _conn(self):
        return self.pool.getconn()

    def _getpool(self):
        pool = psycopg2.pool.ThreadedConnectionPool(2,5, database='postgres', user='postgres', password='open2018', host='112.124.35.123', port='5701')
        return pool

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if not sys.platform.startswith('win'):
        import coloredlogs
        coloredlogs.install(level='DEBUG')

    wxdb = WxDb()
    wxdb.getUnstartedWxRobot()