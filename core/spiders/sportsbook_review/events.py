from datetime import datetime, timedelta

import scrapy
import json

from core.utils import datetime_to_milliseconds

def make_ms(start, end):
    datetime_start = datetime.strptime(start, '%Y-%m-%d')
    datetime_end = datetime.strptime(end, '%Y-%m-%d')
    delta = datetime_end - datetime_start
    dates = [datetime_start + timedelta(i) for i in range(delta.days)]
    ms = [datetime_to_milliseconds(date) for date in dates]
    return ms

class EventSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['sportsbookreview.com']

    def __init__(self):
        self.request_stem = "https://www.sportsbookreview.com/ms-odds-v2/odds-v2-service?query="
        self.core_query = """
        {
            eventsByDateByLeagueGroup( 
                es: ["in-progress", "scheduled", "complete", "suspended", "delayed", "postponed", "retired", "canceled"],
                leagueGroups: [{ mtid: 83, lid: 5, spid: 5 }],
                providerAcountOpener: 3,
                hoursRange: 25,
                showEmptyEvents: false,
                marketTypeLayout: "PARTICIPANTS",
                ic: false,
                startDate: <date>,
                timezoneOffset: -5,
                nof: true,
                hl: true,
                sort: {by: ["lid", "dt", "des"], order: ASC}
                )
                {
                events {
                    eid lid spid des dt es rid ic ven tvs cit cou st sta hl seid writeingame plays(pgid: 2, limitLastSeq: 3, pgidWhenFinished: -1) { eid sqid siid gid nam val tim} participants {
                        eid partid partbeid psid ih rot tr sppil sppic startingPitcher { fn lnam } 
                        source { ... on Player { pid fn lnam } ... on Team { tmid lid tmblid nam nn sn abbr cit senam imageurl } ... on ParticipantGroup { partgid nam lid participants { eid partid psid ih rot source { ... on Player { pid fn lnam } ... on Team { tmid lid nam nn sn abbr cit } } } } } 
                    }
                }
            }
        }
        """

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
        days = make_ms("2014-01-01", "2020-04-01")

        for t in days:
            url = (self.request_stem + self.core_query).replace("\n", "").replace("\t", "").replace('"', '\"')
            self.log("scrape date: " + datetime.utcfromtimestamp(t / 1000).strftime("%Y-%m-%d"))
            url = url.replace("<date>", str(t))
            yield scrapy.Request(url=url, callback=self.parse)



