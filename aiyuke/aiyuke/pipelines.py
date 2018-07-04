# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from w3lib.html import remove_tags
import pymysql
from twisted.enterprise import adbapi
from aiyuke.tools.upload_qiniu import upload
import uuid


class AiyukeIntoTxtPipeline(object):
    def process_item(self, item, spider):
        image_path = os.path.join(os.path.dirname(__file__), "aiyuke")
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_url = item['image_url']

        try:
            pic = requests.get(image_url, timeout=10)
        except:
            print("无法下载图片！")
        file_name = image_path + '/' + uuid.uuid4().hex + '.jpg'
        f = open(file_name, "wb")
        f.write(pic.content)
        f.close()
        image_name = file_name.split('/')[-1]
        a = [item['title'], item['source'], item['datetime'], remove_tags(str(item['content'])), item['cate'], image_name]
        result = ','.join(a)
        with open("aiyuke.txt", "a") as t:
            t.write(result + "\n")
            t.close()

        return item


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', 'root', 'aiyuke', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        image_url = item['image_url']
        # i = len(os.listdir('aiyuke')) + 1
        # file_name = image_path + '/' + 'onlylady_' + str(i) + '.jpg'
        try:
            pic = requests.get(image_url, timeout=10)
        except:
            print("无法下载图片！")
        file_name = 'aiyuke' + '/' + uuid.uuid4().hex + '.jpg'
        f = open(file_name, "wb")
        f.write(pic.content)
        f.close()
        image_name = file_name.split('/')[-1]
        upload(file_name)
        os.remove(file_name)
        qiniu_url = "https://resources.olei.me/aiyuke/{}".format(image_name)

        insert_sql = """
            insert into article(title, source, datetime, content,cate,qiniu_url)
            VALUES (%s, %s, %s, %s,%s,%s)
        """
        self.cursor.execute(insert_sql, (
        item["title"], item["source"], item["datetime"], remove_tags(str(item["content"])), item["cate"], qiniu_url))
        self.conn.commit()

# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host = settings["MYSQL_HOST"],
#             db = settings["MYSQL_DBNAME"],
#             user = settings["MYSQL_USER"],
#             passwd = settings["MYSQL_PASSWORD"],
#             charset='utf8',
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
#
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         #使用twisted将mysql插入变成异步执行
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider) #处理异常
#
#     def handle_error(self, failure, item, spider):
#         # 处理异步插入的异常
#         print (failure)
#
#     def do_insert(self, cursor, item):
#         #执行具体的插入
#         #根据不同的item 构建不同的sql语句并插入到mysql中
#         insert_sql, params = item.get_insert_sql()
#         print (insert_sql, params)
#         cursor.execute(insert_sql, params)
