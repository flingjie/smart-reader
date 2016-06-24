# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class CrawlersPipeline(object):

    def __init__(self):
        client = MongoClient()
        db = client['ai']
        self.col = db['gh']

    def process_item(self, item, spider):
        one = self.col.find_one({"title": item['title']})
        if not one:
            self.col.insert(dict(item))
        return item
