from datetime import datetime
import pytz

import re
import scrapy
import json

from core.sbreview import events_by_date_by_league_group
from core.utils import make_ms, datetime_to_milliseconds


class EventSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['sportsbookreview.com']

    def __init__(self, **kwargs):
        if "date" in kwargs.keys():
            dt = datetime.strptime(kwargs["date"], '%Y-%m-%d')
            self.days = [datetime_to_milliseconds(dt)]
        else:
            self.days = make_ms("2007-01-01", "2020-04-01")

        self.domain = "https://www.sportsbookreview.com"
        self.request_stem = self.domain + "/ms-odds-v2/odds-v2-service?query="
        self.core_query = events_by_date_by_league_group(1)

    def parse(self, response):
        raw_json = json.loads(response.text)
        events = raw_json['data']['eventsByDateByLeagueGroup']['events']
        for event in events:
            event['dt_utc'] = datetime.utcfromtimestamp(event['dt'] / 1000)

            dt_est = event['dt_utc'].replace(tzinfo=pytz.utc)
            dt_est = dt_est.astimezone(pytz.timezone('America/New_York'))
            event['dt_est'] = dt_est.strftime("%Y-%m-%d %H:%M:%S")

            away_at_home = event["des"].split("@")
            event['away'] = away_at_home[0]
            event['home'] = away_at_home[1]
            pid1 = event['participants'][0]['source']
            pid2 = event['participants'][1]['source']
            event['partid_1'] = event['participants'][0]['partid']
            event['partid_2'] = event['participants'][1]['partid']
            event['participant_1'] = pid1['nam'] + ' ' + pid1['nn']
            event['participant_2'] = pid2['nam'] + ' ' + pid2['nn']
            event['participant_1_code'] = pid1['abbr']
            event['participant_2_code'] = pid2['abbr']
            if re.search(event["home"], event["participant_1"]) is not None:
                event["home"] = event["participant_1"]
                event["away"] = event["participant_2"]
                event["home_partid"] = event["partid_1"]
                event["away_partid"] = event["partid_2"]
                event['home_code'] = event['participant_1_code']
                event['away_code'] = event['participant_2_code']
            if re.search(event["home"], event["participant_2"]) is not None:
                event["home"] = event["participant_2"]
                event["away"] = event["participant_1"]
                event["home_partid"] = event["partid_2"]
                event["away_partid"] = event["partid_1"]
                event['home_code'] = event['participant_2_code']
                event['away_code'] = event['participant_1_code']
            yield event

    def start_requests(self):
        for t in self.days:
            url = (self.request_stem + self.core_query).\
                replace("\n", "").\
                replace("\t", "").replace('"', '\"')
            self.log("scrape date: " + datetime.utcfromtimestamp(t / 1000).
                     strftime("%Y-%m-%d"))
            url = url.replace("<date>", str(t))
            yield scrapy.Request(url=url, callback=self.parse)
