import json

import scrapy

from core.sbreview import current_lines
from core.utils import get_eids


class SRMoneyLines(scrapy.Spider):
    name = 'sr_money_lines'
    allowed_domains = ['sportsbookreview.com']

    def __init__(self):
        self.request_stem = "https://www.sportsbookreview.com/ms-odds-v2" \
                            "/odds-v2-service?query= "

    def parse(self, response):
        raw_json = json.loads(response.text)
        events = raw_json['data']['currentLines']
        for event in events:
            yield event

    def start_requests(self):
        events = get_eids()
        queries = [current_lines(event) for event in events]
        urls = [self.request_stem + q for q in queries]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
