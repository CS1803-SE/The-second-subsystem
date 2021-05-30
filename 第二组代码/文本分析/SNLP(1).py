from snownlp import SnowNLP
import pymysql


class MySql:
    def __init__(self, host='localhost', user='', password='', database='', charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = None
        self.cursor = None

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                    charset=self.charset, database=self.database)
        self.cursor = self.conn.cursor()
        print('连接成功：' + self.host + '->' + self.database)

    # 显示当前连接状态
    def connState(self):
        return self.conn

    # 断开连接
    def disconnect(self):
        self.cursor.close()
        self.conn.close()
        print('断开连接')

    # 插入
    def insert(self, sql, para):
        if self.connState() is not None:
            self.cursor.execute(sql, para)
            print('增加成功')

    # 删除
    def delete(self, sql):
        if self.connState() is not None:
            self.cursor.execute(sql)
            print('删除成功')

    # 更新
    def update(self, sql, para):
        return self.__edit(sql, para)

    # 获取一个或多个数据（用于测试）
    def get(self, sql, num=5):
        if self.connState() is not None:
            self.cursor.execute(sql)
            return self.cursor.fetchmany(num)

    # 获取所有数据
    def getAll(self, sql):
        # print(1)
        if self.connState() is not None:
            # print(2)
            self.cursor.execute(sql)
            # print(3)
            return self.cursor.fetchall()

    # 提交更新事务，如果失败则回滚
    def __edit(self, sql, para):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, para)
            self.conn.commit()
            print("成功")
        except Exception:
            print("事物提交失败")
            self.conn.rollback()
            return count


sql1 = """select id,title2 from newsall"""  #
test = MySql(host='120.26.86.149', user='root', password='jk1803_SE', charset='utf8', database='museum_news')
test.connect()

ans = test.getAll(sql1)

for tup in ans:
    txt = "".join(tup[1])
    print(txt)
    if txt.__len__() != 0:
        s = SnowNLP(txt)
        a = round(s.sentiments * 100, 2)
        # print(a)
        data = (a, tup[0])
        print(data)
        sql2 = """update newsall set emotions = %s where id = %s"""
        test.update(sql2, data)

# from snownlp import sentiment
# sentiment.train(
#     'C:\\Users\\86264\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\snownlp\\sentiment\\neg.txt',
#     'C:\\Users\\86264\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\snownlp\\sentiment\\pos.txt')
# sentiment.save(
#     'C:\\Users\\86264\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\snownlp\\sentiment\\sentiment.marshal.3')
