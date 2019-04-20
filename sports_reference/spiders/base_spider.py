import scrapy
import json

# -*- coding: utf-8 -*-
from ..constants import BASKETBALL_REFERENCE_URL

class SRSpider(scrapy.Spider):

    start_url = BASKETBALL_REFERENCE_URL
    allowed_domains = ['basketball-reference.com']

    def __init__(self):
        self.config = None
        super().__init__()

    def configure(self, config_file="config.json"):
        with open(config_file) as f:
            self.config = json.loads(f.read())
