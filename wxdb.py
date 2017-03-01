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
        conn = self._conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = 'select * from wx_hosting h ' \
              'where h.enabled=1 ' \
              'order by h.priority desc;'
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def saveWxChat(self):
        pass

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