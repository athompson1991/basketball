# -*- coding: utf-8 -*-
import re
from datetime import datetime

import bs4
import scrapy

from core.constants import BASKETBALL_REFERENCE_URL, months
from core.items import GameItem
from .base_spider import SRSpider
from core.settings import SEASONS


class GamesSpider(SRSpider):
    name = 'games'

    def __init__(self, **kwargs):
        self.years = SEASONS
        if "year" in kwargs.keys():
            self.years = [kwargs["year"]]
        self.urls = self.generate_urls()

    def generate_urls(self):
        out = []
        for year in self.years:
            for month in months:
                url = BASKETBALL_REFERENCE_URL + "/leagues/NBA_" + str(
                    year) + "_games-" + month + ".html"
                out.append(url)
        return out

    def parse_row(self, row):
        row_data = row.xpath('td|th')
        soup = bs4.BeautifulSoup(row_data[0].extract())
        game_code = soup.find("th")["csk"]
        game_date = datetime.strptime(
            soup.text, "%a, %b %d, %Y"
        ).strftime("%Y-%m-%d")

        soup = bs4.BeautifulSoup(row_data[1].extract())
        start_time = soup.text + 'm'
        start_time = datetime.strptime(start_time, "%I:%M%p").strftime("%H:%M")
        soup = bs4.BeautifulSoup(row_data[2].extract())
        visiting_team = soup.text
        visiting_code = soup.find(href=True).get("href").split("/")[2]
        soup = bs4.BeautifulSoup(row_data[3].extract())
        visitor_points = soup.text
        soup = bs4.BeautifulSoup(row_data[4].extract())
        home_team = soup.text
        home_code = soup.find(href=True).get("href").split("/")[2]
        soup = bs4.BeautifulSoup(row_data[5].extract())
        home_points = soup.text
        soup = bs4.BeautifulSoup(row_data[7].extract())
        has_ot = 'OT' in soup.text
        soup = bs4.BeautifulSoup(row_data[8].extract())
        attendance = soup.text.replace(",", "")

        if int(visitor_points) > int(home_points):
            winner = visiting_code
        elif int(home_points) > int(visitor_points):
            winner = home_code
        else:
            winner = "NA"

        row = GameItem(
            code=game_code,
            game_date=game_date,
            start_time=start_time,
            visiting_team=visiting_team,
            visiting_code=visiting_code,
            visitor_points=visitor_points,
            home_team=home_team,
            home_code=home_code,
            home_points=home_points,
            has_ot=has_ot,
            attendance=attendance,
            winner=winner
        )
        return row

    def parse_item(self, response):
        link = response.url.split("/")[5]
        self.log(link)
        season = int(re.findall(r'\d+', link)[0])
        schedule = response.css("table#schedule")
        schedule_rows = schedule.css("tr")
        for row in schedule_rows[1:]:
            row_item = self.parse_row(row)
            row_item['season'] = season
            yield row_item

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_item)
