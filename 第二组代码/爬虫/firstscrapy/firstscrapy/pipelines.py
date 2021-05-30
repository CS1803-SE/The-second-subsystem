# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter
#import pymsql
#一个管道类对应一种存储方式
class FirstscrapyPipeline:
    fp=None
    # init()为类的初始化方法，开始的时候调用
    def open_spider(self, spider):
        print("开始爬虫。。。。")
        # 首先用写入的方式创建或者打开一个普通文件用于存储爬取到的数据
        self.fp = open("./hellow.txt", "w",encoding="utf-8")

    # processitem（）为pipelines中的主要处理方法，默认会自动调用
    def process_item(self, item, spider):
        # 设置每行要写的内容
        title = item["title"]
        time = item["time"]
        c = item["content"]
        author= item["author"]
        museum = item["museum"]
        detail_url = item['detail_url']
        if  not re.search(museum, c):
            pass
        # 将对应信息写入文件中
        self.fp.write(title+"\n"+time+"\n"+author+"\n"+detail_url+"\n"+c+"\n"+"\n")
        return item

    def close_spider(self, spider):
        # 关闭文件
        print("文件关闭")
        self.fp.close()



    # # 每接收到一个item就被调用一次
    # def process_item(self, item, spider):
    #     title = item['title']
    #     return item
    #
    # def close_spider(self, spider):
    #     print("结束爬虫！")


'''
存储数据到数据库
'''


# class MysqlPipeline(object):
#     # connect = None
#     # cursor = None
#     #
#     # def open_spider(self, spider):
#     #     self.connect = pymysql.Connect(
#     #         # host='localhost',
#     #         # port=3306,
#     #         # user='root',
#     #         # password='mysql',
#     #         # db='group2-zjf-news',
#     #         # charset='utf8'
#     #         host='151.106.117.0',
#     #         port=3306,
#     #         user='u987603792_news',
#     #         password='Newsnews2',
#     #         db='news',
#     #         charset='utf8'
#     #     )
#     #
#     def process_item(self, item, spider):
#     #     title = item['title']
#     #     author = item['author']
#     #     time = item['time']
#     #     #description = item['description']
#     #     content = item['content']
#     #     detail_url = item['detail_url']
#     #     #tag = item['tag']
#     #     self.cursor = self.connect.cursor()
#     #
#     #     try:
#     #         self.cursor.execute(
#     #             "select title from news where title ='{}'".format(title)
#     #         )
#     #         repetiton = self.cursor.fetchone()
#     #         if repetiton:
#     #             pass
#     #         else:
#     #             self.cursor.execute(
#     #                 "insert into news(title, author, time,  content, url) values ('{}','{}','{}','{}','{}')".format(
#     #                     title, author, time,  content, detail_url
#     #                 )
#     #             )
#     #             self.connect.commit()
#     #     except Exception as error:
#     #         print(error)
#     #         self.connect.rollback()
#     #
#     #
#     #
#     #     return item
#     #
#     # def close_spider(self, spider):
#     #     self.cursor.close()
#     #     self.connect.close()