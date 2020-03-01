import csv
import datetime

import psycopg2

from config import output_directory
from core.settings import database_specs
from core.utils import make_create_sql, make_insert_sql


class CSVPipeline(object):
    def __init__(self):
        self.time_format = "%Y-%m-%d_%H%M%S"
        self.fieldnames = {
            "games": ["code", "game_date", "start_time", "home_team", "home_code", "home_points", "visiting_team",
                      "visiting_code", "visitor_points", "has_ot", "attendance", "winner"],
            "pbp": ["code", "quarter", "time", "team", "player_1", "player_2", "player_1_name", "player_2_name",
                    "score", "home_score", "away_score", "play"],
            "boxscore": ['code', 'team', 'player_code', 'player', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
                         'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts',
                         'plus_minus', 'reason'],
            "shotchart": ['code', 'player_code', 'team', 'team_type', 'shot_location', 'x', 'y', 'made_shot', 'tip',
                          'quarter', 'time_left'],
            "line_movements": ['league', 'game_id']
        }

    def open_spider(self, spider):
        spider_name = spider.name
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        target_dir = output_directory + "/" + spider_name + "/"
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


class PostgresPipeline(object):

    def open_spider(self, spider):
        self.create_table_sql = make_create_sql(spider.name, database_specs['tables'][spider.name])
        self.client = psycopg2.connect(
            host=database_specs['host'],
            database=database_specs['database'],
            user=database_specs['user'],
            password=database_specs['password']
        )
        cursor = self.client.cursor()
        cursor.execute("drop table if exists " + spider.name)
        cursor.close()
        self.client.commit()
        cursor = self.client.cursor()
        cursor.execute(self.create_table_sql)
        cursor.close()
        self.client.commit()

    def process_item(self, item, spider):
        sql_specs = database_specs['tables'][spider.name]
        cursor = self.client.cursor()
        self.insert_game_sql = make_insert_sql(spider.name, sql_specs)
        insert_this = {key: item[key] for key in sql_specs.keys()}
        cursor.execute(self.insert_game_sql, insert_this)
        cursor.close()
        self.client.commit()

    def close_spider(self, spider):
        self.client.commit()
        self.client.close()
