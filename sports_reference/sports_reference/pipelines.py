# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
from .decorators import check_spider_pipeline
from .decorators import check_spider_pipeline_file
from scrapy.exceptions import DropItem

time_format = "%Y-%m-%d_%H%M%S"

class SportsReferencePipeline(object):
    def process_item(self, item, spider):
        return item


class GamesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    @check_spider_pipeline_file
    def open_spider(self, spider):
        now = datetime.datetime.now()
        now_str = now.strftime(time_format)
        filename = "games_" + now_str + ".csv"
        self.file = open("games/" + filename, 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=[
                "code",
                "game_date",
                "start_time",
                "home_team",
                "home_code",
                "home_points",
                "visiting_team",
                "visiting_code",
                "visitor_points",
                "has_ot",
                "attendance"
            ],
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

    @check_spider_pipeline_file
    def close_spider(self, spider):
        self.file.close()

class PlaybyplayPipeline(object):

    @check_spider_pipeline_file
    def open_spider(self, spider):
        now = datetime.datetime.now()
        now_str = now.strftime(time_format)
        self.file = open("pbp/pbp_" + now_str + ".csv", 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames = [
                "code",
                "quarter",
                "time",
                "team",
                "player_codes",
                "player_names",
                "score",
                "play"
            ],
            lineterminator='\n'
        )
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))

    @check_spider_pipeline_file
    def close_spider(self, spider):
        self.file.close()

class BoxscorePipeline(object):
    @check_spider_pipeline_file
    def open_spider(self, spider):
        now = datetime.datetime.now()
        now_str = now.strftime(time_format)
        filename = "boxscore_" + now_str + ".csv"
        self.file = open("boxscore/" + filename, 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=[
                'code',
                'team',
                'player',
                'mp',
                'fg',
                'fga',
                'fg_pct',
                'fg3',
                'fg3a',
                'fg3_pct',
                'ft',
                'fta',
                'ft_pct',
                'orb',
                'drb',
                'trb',
                'ast',
                'stl',
                'blk',
                'tov',
                'pf',
                'pts',
                'plus_minus',
                'reason'
            ],
            lineterminator='\n'
        )
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))

    @check_spider_pipeline_file
    def close_spider(self, spider):
        self.file.close()