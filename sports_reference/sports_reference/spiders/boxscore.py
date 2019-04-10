# -*- coding: utf-8 -*-
import scrapy
import bs4
from ..pipelines import BoxscorePipeline
from ..items import BoxscoreItem
from ..utils import get_codes

class BoxscoreSpider(scrapy.Spider):
    name = 'boxscore'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    pipeline = set([BoxscorePipeline])

    def __init__(self):
        self.teams = None

    def parse(self, response):
        code = response.url.split("/")[-1][:-5]
        self.log("Code: " + str(code))
        scorebox = response.css("div.scorebox")
        teams = scorebox.xpath("//strong//a/@href").extract()
        self.teams = [t.split("/")[-2] for t in teams]
        for team in self.teams:
            self.log("Code: {0}, team: {1}".format(code, team))
            find_this = "table#box_" + team.lower() + "_basic"
            basic_table = response.css(find_this)
            basic_table_body = basic_table.css("tbody")
            body_rows = basic_table_body[0].css("tr")
            for row in body_rows:
                soup = bs4.BeautifulSoup(row.extract())
                tds = soup.find_all("td")
                stats = {td["data-stat"]: td.text for td in tds}
                player = soup.find("th").text
                stats["code"] = code
                stats["player"] = player
                stats["team"] = team
                item = BoxscoreItem(stats)
                if player != "Reserves":
                    yield item

    def start_requests(self):
        url_stem = "https://www.basketball-reference.com/boxscores/"
        codes = get_codes()
        urls = [url_stem + code + ".html" for code in codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
