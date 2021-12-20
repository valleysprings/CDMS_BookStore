# 数据库连接对象
import pymysql
import threading
from queue import Queue
from dbutils.pooled_db import PooledDB

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "root",
    "db": "bookstore",
    "charset": "utf8"
}
connPool = PooledDB(pymysql, 
    4, 
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    user=DB_CONFIG["user"],
    passwd=DB_CONFIG["passwd"],
    db=DB_CONFIG["db"],
    charset=DB_CONFIG["charset"]
)

class Dao(object):
    def get_cursor(self):
        # lock.acquire()
        return self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def close_cursor(self):
        self.cursor.close()
        # lock.release()

    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multi_modify(self, sql, args=None):
        self.cursor.executemany(sql, args)
        self.conn.commit()