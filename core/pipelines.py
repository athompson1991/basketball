import csv
import datetime

from core.settings import OUTPUT_DIRECTORY
from core.db import database_specs


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


