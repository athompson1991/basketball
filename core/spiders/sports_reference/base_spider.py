import bs4
import requests
import scrapy
import string

# -*- coding: utf-8 -*-
from core.constants import BASKETBALL_REFERENCE_URL


class SRSpider(scrapy.Spider):
    name = "base"
    start_url = BASKETBALL_REFERENCE_URL
    allowed_domains = ['basketball-reference.com']

    def __init__(self):
        super().__init__()
        self.teams_url = BASKETBALL_REFERENCE_URL + "/teams/"
        self.players_url = BASKETBALL_REFERENCE_URL + "/players/"
        self.boxscore_url = BASKETBALL_REFERENCE_URL + "/boxscores/"

    def get_team_codes(self, response):
        scorebox = response.css('div.scorebox')
        soup = bs4.BeautifulSoup(scorebox[0].extract())
        teams = soup.find_all('strong')
        home_href = teams[1].find_all('a', href=True)[0]['href']
        visit_href = teams[0].find_all('a', href=True)[0]['href']
        home_team = home_href.split("/")[2]
        visiting_team = visit_href.split("/")[2]
        return (home_team, visiting_team)

    def get_codes(self):
        response = requests.get(self.teams_url)
        soup = bs4.BeautifulSoup(response.text)
        teams_active = soup.find(id="teams_active")
        rows = teams_active.find_all('tr')
        codes = []
        for row in rows:
            a = row.find('a')
            if a is not None:
                code = a.get("href").split('/')[2]
                codes.append(code)
        return codes

    def check_dict(self, item,  db_table):
        numeric_types = ['integer', 'double precision']
        keys = db_table.keys()
        for k in keys:
            dtype = db_table[k]['dtype']
            if k not in item.keys():
                item[k] = None
            if dtype in numeric_types:
                if item[k] == '':
                    item[k] = 0
                try:
                    item[k] = float(item[k])
                except:
                    print("key: " + str(k))
        return item
