import csv
import datetime

from core.settings import OUTPUT_DIRECTORY
from core.db import database_specs
from core.utils import make_create_sql, make_insert_sql, create_connection


class CSVPipeline(object):
    def __init__(self):
        self.time_format = "%Y-%m-%d_%H%M%S"

    def open_spider(self, spider):
        spider_name = spider.name
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        target_dir = OUTPUT_DIRECTORY + "/" + spider_name + "/"
        filename = target_dir + spider_name + "_" + now_str + ".csv"
        self.file = open(filename, 'w')
        self.colnames = database_specs['tables'][spider_name].keys()
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=self.colnames,
            lineterminator='\n'
        )
        self.writer.writeheader()

    def process_item(self, item, spider):
        item = dict(item)
        row = {col: item[col] for col in self.colnames}
        self.writer.writerow(row)

    def close_spider(self, spider):
        self.file.close()


class PostgresPipeline(object):

    def open_spider(self, spider):
        self.create_table_sql = make_create_sql(
            spider.name,
            database_specs['tables'][spider.name]
        )
        self.client = create_connection()
        cursor = self.client.cursor()
        cursor.execute('drop table if exists ' + spider.name)
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
