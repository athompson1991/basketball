# -*- coding: utf-8 -*-
import scrapy
import bs4
import csv
from ..items import PlaybyplayItem
from ..pipelines import PlaybyplayPipeline
import os
import re
from datetime import datetime

class PlaybyplaySpider(scrapy.Spider):
    name = 'playbyplay'

    pipeline = set([PlaybyplayPipeline])

    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    def __init__(self, debug=True):
        self.DEBUG = debug

    def get_most_recent_scrape(self):
        regex_pattern = '%Y-%m-%d_%H%M%S'
        regex = re.compile(r'\.csv')
        files = os.listdir("games")
        csv_files = list(filter(regex.search, files))
        dates = [datetime.strptime(f, "games_" + regex_pattern + ".csv") for f in csv_files]
        mdate = max(dates)
        not_max = list(filter(lambda x: x != mdate, dates))
        if len(not_max) > 0:
            out = "games_" + max(not_max).strftime("%Y-%m-%d_%H%M%S") + ".csv"
        else:
            out = "NA"
        return out



    def get_codes(self):
        most_recent_scrape = self.get_most_recent_scrape()
        if most_recent_scrape != "NA":
            with open("./games/" + most_recent_scrape, 'r', newline='') as f:
                reader = csv.DictReader(f)
                out = [row['code'] for row in reader]
            if self.DEBUG:
                out = out[:50]
        else:
            out = ["200803010ORL"]
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
        quarter = None
        for row in rows:
            ids =  row.xpath("@id").extract()
            if len(ids) > 0:
                quarter = ids[0]
            td_ls = row.css('td')
            if len(td_ls) == 6:
                time = td_ls[0].xpath("text()")[0].extract()

                home_soup = bs4.BeautifulSoup(td_ls[1].extract())
                home_play = home_soup.text

                score = td_ls[3].xpath("text()")[0].extract()
                visit_soup = bs4.BeautifulSoup(td_ls[5].extract())
                visit_play = visit_soup.text

                if home_play.strip() == "":
                    team = "visitor"
                    play = visit_play
                    players = visit_soup.find_all("a")
                    players_codes = [player.get("href").split("/")[3][:-5] for player in players]
                    player_names = [player.text for player in players]

                if home_play.strip() != "":
                    team = "home"
                    play = home_play
                    players = home_soup.find_all("a")
                    players_codes = [player.get("href").split("/")[3][:-5] for player in players]
                    player_names = [player.text for player in players]

                i = 1
                for player in player_names:
                    play = play.replace(player, "player_" + str(i))
                    i = i + 1

                item = PlaybyplayItem(
                    code = code,
                    quarter = quarter,
                    time = time,
                    team = team,
                    play = play,
                    player_codes = players_codes,
                    player_names = player_names,
                    score = score
                )
                yield item


def get_most_recent_scrape():
    regex_pattern = '%Y-%m-%d_%H%M%S'
    regex = re.compile(r'\.csv')
    files = os.listdir("games")
    csv_files = list(filter(regex.search, files))
    dates = [datetime.strptime(f, "games_" + regex_pattern + ".csv") for f in csv_files]
    return "games_" + max(dates).strftime("%Y-%m-%d_%H%M%S") + ".csv"