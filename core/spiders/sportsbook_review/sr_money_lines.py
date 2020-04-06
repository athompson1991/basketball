from datetime import datetime, timedelta

import scrapy
import json

from core.utils import get_eids


class SRMoneyLines(scrapy.Spider):
    name = 'sr_money_lines'
    allowed_domains = ['sportsbookreview.com']

    def __init__(self):
        self.request_stem = "https://www.sportsbookreview.com/ms-odds-v2/odds-v2-service?query="
        self.core_query = """
        {
            currentLines(
                eid: <key>,
                mtid: [83],
                marketTypeLayout: "PARTICIPANTS", catid: 133
            )
        }
        """

    def parse(self, response):
        raw_json = json.loads(response.text)
        events = raw_json['data']['currentLines']
        for event in events:
            yield event

    def start_requests(self):
        url = (self.request_stem + self.core_query).replace("\n", "").replace("\t", "").replace('"', '\"')
        events = get_eids()
        urls = [url.replace("<key>", str(event)) for event in events]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
