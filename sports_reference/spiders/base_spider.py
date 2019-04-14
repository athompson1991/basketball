import scrapy
import json

class SRSpider(scrapy.Spider):
    def __init__(self):
        self.config = None
        super().__init__()

    def configure(self, config_file="config.json"):
        with open(config_file) as f:
            self.config = json.loads(f.read())
