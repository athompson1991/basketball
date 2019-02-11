# -*- coding: utf-8 -*-
import scrapy
import bs4
import requests


class PlaybyplaySpider(scrapy.Spider):
    name = 'playbyplay'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    def start_requests(self):
        urls = [
            "https://www.basketball-reference.com/boxscores/pbp/201810160BOS.html",
            "https://www.basketball-reference.com/boxscores/pbp/201810160GSW.html"
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        game = response.url.split("/")[-1]
        pbp_table = response.css("table#pbp").extract_first()
        pbp_soup = bs4.BeautifulSoup(pbp_table, "html.parser")
        filename = "pbp-%s" % game
        with open(filename, 'wb') as f:
            f.write(pbp_soup.extract().encode('utf-8'))
        
        