# coding:utf-8

import pymysql

import mysqlSetting


class MysqlDB(object):
    def __init__(self,
                 table,
                 database=mysqlSetting.DATABASE,
                 host=mysqlSetting.HOST,
                 port=mysqlSetting.PORT,
                 user=mysqlSetting.USER,
                 passwd=mysqlSetting.PASSWD):
        self.database = database
        self.host = host
        self.port = port
        self.passwd = passwd
        self.table = table

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, bd=self.database, charset='utf-8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            print('connect mysql error')

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            print(sql + 'execute failed.')
        return None

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误时回滚
            self.database.rollback()
            print(e)
            print(sql + 'execute failed.')

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            print('Close %s successfully.' % self.database)
        except Exception as e:
            print(e)
            print('Failed to close %s.' % self.database)
