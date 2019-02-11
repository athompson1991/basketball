# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from .decorators import check_spider_pipeline
from scrapy.exceptions import DropItem


class SportsReferencePipeline(object):
    def process_item(self, item, spider):
        return item


class GamesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        self.file = open("games.csv", 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=["code", "start_time", "home_team", "visiting_team"],
            lineterminator='\n'
        )
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        if item["code"] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item["code"])
            self.writer.writerow(dict(item))

    def close_spider(self, spider):
        self.file.close()

class PlaybyplayPipeline(object):

    def open_spider(self, spider):
        self.file = open("play_by_play.csv", 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=["code", "time"],
            lineterminator='\n'
        )
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))

    def close_spider(self, spider):
        self.file.close()