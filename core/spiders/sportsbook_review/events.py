from datetime import datetime

import scrapy
import json

from core.sbreview import events_by_date_by_league_group
from core.utils import make_ms


class EventSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['sportsbookreview.com']

    def __init__(self):
        self.request_stem = \
            "https://www.sportsbookreview.com/ms-odds-v2/odds-v2-service?" \
            "query="
        self.core_query = events_by_date_by_league_group(1)

    def parse(self, response):
        raw_json = json.loads(response.text)
        events = raw_json['data']['eventsByDateByLeagueGroup']['events']
        for event in events:
            event['dt'] = datetime.utcfromtimestamp(event['dt'] / 1000)
            home = event['participants'][0]['source']
            away = event['participants'][1]['source']
            event['home_partid'] = event['participants'][0]['partid']
            event['away_partid'] = event['participants'][1]['partid']
            event['home_team'] = home['nam'] + ' ' + home['nn']
            event['away_team'] = away['nam'] + ' ' + away['nn']
            event['home_code'] = home['abbr']
            event['away_code'] = away['abbr']
            yield event

    def start_requests(self):
        days = make_ms("2007-01-01", "2020-04-01")
        for t in days:
            url = (self.request_stem + self.core_query).replace("\n", "").\
                replace("\t", "").replace('"', '\"')
            self.log("scrape date: " + datetime.utcfromtimestamp(t / 1000).
                     strftime("%Y-%m-%d"))
            url = url.replace("<date>", str(t))
            yield scrapy.Request(url=url, callback=self.parse)
