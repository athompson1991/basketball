# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
from scrapy.exceptions import DropItem


class CSVPipeline(object):
    def __init__(self):
        self.time_format = "%Y-%m-%d_%H%M%S"
        self.fieldnames= {
            "games": ["code", "game_date", "start_time", "home_team", "home_code", "home_points", "visiting_team", "visiting_code", "visitor_points", "has_ot","attendance", "winner"],
            "pbp": ["code", "quarter", "time", "team", "player_codes", "player_names", "score", "play" ],
            "boxscore": ['code', 'team', 'player', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'plus_minus', 'reason' ],
            "shotchart": ['code', 'home_team', 'visiting_team']
        }

    def open_spider(self, spider):
        spider_name = spider.name
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        target_dir = "data/" + spider_name + "/"
        filename = target_dir + spider_name + "_" + now_str + ".csv"
        self.file = open(filename, 'w')
        self.writer = csv.DictWriter(
           self.file,
           fieldnames=self.fieldnames[spider_name],
           lineterminator='\n'
        )
        self.writer.writeheader()

    def process_item(self, item, spider):
            self.writer.writerow(dict(item))

    def close_spider(self, spider):
        self.file.close()

