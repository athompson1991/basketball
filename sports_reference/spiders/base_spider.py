import scrapy
import json
import bs4

# -*- coding: utf-8 -*-
from ..constants import BASKETBALL_REFERENCE_URL

class SRSpider(scrapy.Spider):

    start_url = BASKETBALL_REFERENCE_URL
    allowed_domains = ['basketball-reference.com']
    debug = True

    def __init__(self):
        self.config = None
        super().__init__()

    def configure(self, config_file="config.json"):
        with open(config_file) as f:
            self.config = json.loads(f.read())

    def get_team_codes(self, response):
        scorebox = response.css('div.scorebox')
        soup = bs4.BeautifulSoup(scorebox[0].extract())
        teams = soup.find_all('strong')
        home_href = teams[1].find_all('a', href=True)[0]['href']
        visit_href = teams[0].find_all('a', href=True)[0]['href']

        home_team = home_href.split("/")[2]
        visiting_team = visit_href.split("/")[2]
        return (home_team, visiting_team)


