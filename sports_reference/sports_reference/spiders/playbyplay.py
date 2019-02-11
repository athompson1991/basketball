# -*- coding: utf-8 -*-
import scrapy
import bs4
import csv

class PlaybyplaySpider(scrapy.Spider):
    name = 'playbyplay'

    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    def get_codes(self):
        with open('../../games.csv', 'r', newline='') as f:
            reader = csv.DictReader(f)
            out = [row['code'] for row in reader]
        return out

    def start_requests(self):
        codes = self.get_codes()
        url_stem = "https://www.basketball-reference.com/boxscores/pbp/"
        urls = [url_stem + code + ".html" for code in codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        game = response.url.split("/")[-1]
        pbp_table = response.css("table#pbp").extract_first()
        pbp_soup = bs4.BeautifulSoup(pbp_table, "html.parser")
        filename = "pbp-%s" % game
        