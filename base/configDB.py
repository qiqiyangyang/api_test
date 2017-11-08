import pymysql
import pymssql
import readConfig as readConfig
from base.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

class MyDB:
    #获取数据库配置
    global host, username, password, port, database, config
    host = localReadConfig.get_db("host")
    username = localReadConfig.get_db("username")
    password = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    config = {
        'host': str(host),
        'user': username,
        'password': password,
        'port': int(port),
        'database': database
    }
    #初始化
    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    #建立数据库连接,这里是mysql的连接
    def connectDB(self):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB

            #self.db = pymysql.connect(**config)
            self.db = pymssql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

        return self.cursor

    #数据库查询操作
    def executeSQL(self, sql,params):
        """
        execute sql
        :param sql:
        :return:
        """
        if self.cursor is None:
            self.cursor = self.connectDB()
            self.cursor.execute(sql,params)
        else:
            self.cursor.execute(sql, params)
        return self.cursor

    #返回所有数据
    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    #返回一条数据
    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    #关闭连接
    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        self.cursor=None
        print("Database closed!")

if __name__=='__main__':
    db=MyDB()
    params=('13249824552')
    print (list(db.get_all(db.executeSQL('select * from T_User where Tel=%s',params))))
    print(list(db.get_one(db.executeSQL('select * from T_User',None))))
    db.closeDB()