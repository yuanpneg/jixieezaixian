import pymysql as ps
import pymysql.cursors


class MysqlHelper:
    def __init__(self, host, user, password, database, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None

    # 数据库连接
    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                             charset=self.charset, cursorclass=ps.cursors.DictCursor)
        self.curs = self.db.cursor()

    # 数据库关闭
    def close(self):
        self.curs.close()
        self.db.close()

    # 数据增删改
    def cud(self, sql):
        self.open()
        try:
            self.curs.execute(sql)
            self.db.commit()
        except Exception as e:
            print(repr(e))
            self.db.rollback()
        finally:
            self.close()

    # 数据查询list
    def find(self, sql):
        self.open()
        try:
            self.curs.execute(sql)
            list = self.curs.fetchall()
            self.close()
            return list
        except Exception as e:
            print(repr(e))
            print('find出现错误')

    def find_id(self, sql):
        self.open()
        try:
            id = self.curs.execute(sql)
            self.close()
            return id
        except Exception as e:
            print(repr(e))
            print('find出现错误')
