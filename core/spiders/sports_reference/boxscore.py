# -*- coding: utf-8 -*-
import bs4
import scrapy

from core.constants import BASKETBALL_REFERENCE_URL
from core.items import BoxscoreItem
from .base_spider import SRSpider
from ...utils import get_codes


class BoxscoreSpider(SRSpider):
    name = 'boxscore'

    def __init__(self, **kwargs):
        super().__init__()
        self.teams = None
        if "code" in kwargs.keys():
            self.codes = [kwargs["code"]]
        else:
            self.codes = get_codes()

    def get_teams(self, soup):
        scorebox = soup.find('div', {'class': 'scorebox'})
        strongs = scorebox.find_all("strong")
        hrefs = [strong.find("a").get("href") for strong in strongs]
        teams = [href.split("/")[-2] for href in hrefs]
        return teams

    def minutes_played_num(self, mp):
        t = mp.split(':')
        return float(t[0]) + float(t[1]) / 60

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text)
        code = response.url.split("/")[-1][:-5]
        teams = self.get_teams(soup)
        for team in teams:
            self.log("Code: {0}, team: {1}".format(code, team))
            find_this = "table#box-" + team.upper() + "-game-basic"
            basic_table = response.css(find_this)
            basic_table_body = basic_table.css("tbody")
            body_rows = basic_table_body[0].css("tr")
            for row in body_rows:
                soup = bs4.BeautifulSoup(row.extract())
                player = soup.find("th").text

                if player != "Reserves":
                    th = soup.find_all('th')
                    player_code = th[0].attrs['data-append-csv']
                    tds = soup.find_all("td")
                    if(len(tds) < 10):
                        print("DID NOT PLAY")
                        break
                    stats = {td["data-stat"]: td.text for td in tds}
                    stats["code"] = code
                    stats["player"] = player
                    stats["team"] = team
                    stats['player_code'] = player_code
                    stats['mp_num'] = self.minutes_played_num(stats['mp'])
                    item = BoxscoreItem(stats)
                    yield item

    def start_requests(self):
        urls = [self.boxscore_url + code + ".html" for code in self.codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
