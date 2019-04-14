# -*- coding: utf-8 -*-
import scrapy
import bs4
from ..items import BoxscoreItem
from .base_spider import SRSpider
from ..constants import BASKETBALL_REFERENCE_URL

class BoxscoreSpider(SRSpider):
    name = 'boxscore'
    allowed_domains = ['basketball-reference.com']
    start_urls = [BASKETBALL_REFERENCE_URL]

    def __init__(self):
        self.teams = None
        self.configure()
        self.codes = self.config['boxscore']['codes']

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
        url_stem = BASKETBALL_REFERENCE_URL + "/boxscores/"
        urls = [url_stem + code + ".html" for code in self.codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
