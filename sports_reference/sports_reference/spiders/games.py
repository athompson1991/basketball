# -*- coding: utf-8 -*-
import scrapy
import bs4

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from..items import GameItem

class GamesSpider(CrawlSpider):
    name = 'games'
    
    years = range(1990, 2019)
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
        soup = bs4.BeautifulSoup(row_data[1].extract())
        start_time = soup.text
        soup = bs4.BeautifulSoup(row_data[2].extract())
        visiting_team = soup.text
        soup = bs4.BeautifulSoup(row_data[4].extract())
        home_team = soup.text
        row = GameItem(
            code = game_code,
            start_time = start_time,
            visiting_team = visiting_team,
            home_team = home_team
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
        
