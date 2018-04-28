# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from book_sacrpy.items import BookItem

class BookIntodbPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect("localhost","root","root","book",charset="utf8")
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        insert_sql = '''
            insert into book(title,isbn,price) VALUES ('{}','{}','{}')
        '''
        self.cursor.execute(insert_sql.format(item['title'],item['isbn'],item['price']))
        self.conn.commit()
        # return item
