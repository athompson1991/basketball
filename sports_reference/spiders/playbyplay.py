# -*- coding: utf-8 -*-
import scrapy
import bs4
from ..items import PlaybyplayItem
from ..pipelines import PlaybyplayPipeline
from ..utils import get_codes

class PlaybyplaySpider(scrapy.Spider):
    name = 'playbyplay'

    pipeline = set([PlaybyplayPipeline])

    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    DEBUG = True

    def start_requests(self):
        url_stem = "https://www.basketball-reference.com/boxscores/pbp/"
        codes = get_codes()
        if self.DEBUG:
            urls = [url_stem + "200803010ORL.html"]
        else:
            urls = [url_stem + code + ".html" for code in codes]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_left_or_right(self, td, type):
        out = {}
        soup = bs4.BeautifulSoup(td.extract())
        out["play"] = soup.text
        if out["play"].strip() != "":
            out["team"] = type
            out["players"] = soup.find_all("a")
            out["players_codes"] = [player.get("href").split("/")[3][:-5] for player in out["players"]]
            out["player_names"] = [player.text for player in out["players"]]
        else:
            out = None
        return out

    def parse(self, response):
        code = response.url.split("/")[-1][:-5]
        pbp_table = response.css("table#pbp")
        rows = pbp_table.xpath("//tr")
        quarter = None
        for row in rows:
            ids =  row.xpath("@id").extract()
            if len(ids) > 0:
                quarter = ids[0]
            td_ls = row.css('td')
            if len(td_ls) == 6:
                time = td_ls[0].xpath("text()")[0].extract()
                score = td_ls[3].xpath("text()")[0].extract()

                left_and_right = [
                    self.parse_left_or_right(td_ls[1], "home"),
                    self.parse_left_or_right(td_ls[5], "visitor")
                ]

                non_null = [td for td in left_and_right if td is not None][0]

                item = PlaybyplayItem(
                    code = code,
                    quarter = quarter,
                    time = time,
                    team = non_null["team"],
                    play = non_null["play"],
                    player_codes = non_null["players_codes"],
                    player_names = non_null["player_names"],
                    score = score
                )
                yield item
