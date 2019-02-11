# -*- coding: utf-8 -*-
import scrapy
import bs4
import csv
from ..items import PlaybyplayItem
from ..pipelines import PlaybyplayPipeline

class PlaybyplaySpider(scrapy.Spider):
    name = 'playbyplay'

    pipeline = set([PlaybyplayPipeline])

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
        code = response.url.split("/")[-1][:-5]
        pbp_table = response.css("table#pbp")
        rows = pbp_table.xpath("//tr")
        for row in rows:
            td_ls = row.css('td')
            if len(td_ls) > 0:
                time = td_ls[0].extract()
                item = PlaybyplayItem(code = code, time = time)
                yield item

        