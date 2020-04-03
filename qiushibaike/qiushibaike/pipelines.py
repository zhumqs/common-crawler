# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class QiushibaikePipeline(object):

    def __init__(self):
        print("init mongo connection!!!!!!")
        self.connection = pymongo.MongoClient('localhost', 27017)
        print(self.connection)
        # use DATABASE_NAME 创建数据库
        self.db = self.connection.scrapy
        print(self.db)
        # db.COLLECTION_NAME.insert(document) 向集合中插入文档
        self.qiushibaike = self.db.qiushibaike
        print(self.qiushibaike)

    def process_item(self, item, spider):
        if not self.connection or not item:
            return
        self.qiushibaike.save(item)

    def __del__(self):
        if self.connection:
            self.connection.close()


