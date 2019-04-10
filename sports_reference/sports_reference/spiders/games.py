# -*- coding: utf-8 -*-
import scrapy
import bs4

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from..items import GameItem
from ..pipelines import GamesPipeline



class GamesSpider(CrawlSpider):
    name = 'games'

    pipeline = set([GamesPipeline])

    years = range(2017, 2019)
    allowed_domains = ['basketball-reference.com']
    start_urls = ["https://www.basketball-reference.com/leagues/NBA_" + str(i) + "_games.html" for i in years]
    follow_urls = ['/leagues/NBA_' + str(i) + '_games' for i in years]

    rules = (
        [Rule(LinkExtractor(allow=i), callback='parse_item', follow=False) for i in follow_urls]
    )
 
    def parse_row(self, row):
        row_data = row.xpath('td|th')
        data_names = [d.xpath("@data-stat").get() for d in row_data]
        soup = bs4.BeautifulSoup(row_data[0].extract())
        game_code = soup.find("th")["csk"]
        game_date = datetime.strptime(
            soup.text, "%a, %b %d, %Y"
        ).strftime("%Y-%m-%d")

        soup = bs4.BeautifulSoup(row_data[1].extract())
        start_time = soup.text
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
        has_ot = soup.text == 'OT'
        soup = bs4.BeautifulSoup(row_data[8].extract())
        attendance = soup.text.replace(",", "")

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
            attendance=attendance
        )
        return row

    def parse_item(self, response):
        link = response.url.split("/")[4]
        self.log(link)
        schedule = response.css("table#schedule")
        schedule_rows = schedule.css("tr")
        for row in schedule_rows[1:]:
            row_item = self.parse_row(row)
            yield row_item

