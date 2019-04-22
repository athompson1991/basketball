# -*- coding: utf-8 -*-
"""Play by Play data
This module contains the spider that gets the play-by-play schedule for a full game
from the basketball-reference website.
"""
import scrapy
import bs4
from ..items import PlaybyplayItem
from .base_spider import SRSpider
from ..constants import BASKETBALL_REFERENCE_URL

class PlaybyplaySpider(SRSpider):
    """PlaybyplaySpider does the parsing of the response

    """
    name = 'pbp'

    def __init__(self):
        """Initialization includes reading the config file
        """
        super().__init__()
        self.configure()
        if self.debug:
            self.codes = self.config['pbp']['debug_codes']
        else:
            self.codes = self.config['pbp']['codes']

    def start_requests(self):
        url_stem = BASKETBALL_REFERENCE_URL + "/boxscores/pbp/"
        urls = [url_stem + code + ".html" for code in self.codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def get_player_codes(self, soup):
        players = soup.find_all("a")
        players_codes = [player.get("href").split("/")[3][:-5] for player in players]
        player_names = [player.text for player in players]
        n = len(players_codes)
        if n == 1:
            player_1 = players_codes[0]
            player_2 = ''
            player_1_name = player_names[0]
            player_2_name = ''
        elif n == 2:
            player_1 = players_codes[0]
            player_2 = players_codes[1]
            player_1_name = player_names[0]
            player_2_name = player_names[1]
        elif n == 0:
            player_1 = ''
            player_2 = ''
            player_1_name = ''
            player_2_name = ''
        return (player_1, player_2, player_1_name, player_2_name)

    def parse_left_or_right(self, td, team_type):
        out = {}
        soup = bs4.BeautifulSoup(td.extract())
        out["play"] = soup.text
        if out["play"].strip() != "":
            out["team"] = team_type
            out["player_1"], out["player_2"], out["player_1_name"], out["player_2_name"] = self.get_player_codes(soup)
        else:
            out = None
        return out

    def parse(self, response):
        code = response.url.split("/")[-1][:-5]
        home_team, visiting_team = self.get_team_codes(response)

        pbp_table = response.css("table#pbp")
        rows = pbp_table.xpath("//tr")
        quarter = None
        for row in rows:
            ids = row.xpath("@id").extract()
            if len(ids) > 0:
                quarter = ids[0]
            td_ls = row.css('td')
            if len(td_ls) == 6:
                time = td_ls[0].xpath("text()")[0].extract()
                score = td_ls[3].xpath("text()")[0].extract()
                score_split = score.split('-')
                home_score = score_split[0]
                away_score = score_split[1]

                left_and_right = [
                    self.parse_left_or_right(td_ls[1], home_team),
                    self.parse_left_or_right(td_ls[5], visiting_team)
                ]

                non_null = [td for td in left_and_right if td is not None][0]

                item = PlaybyplayItem(
                    code=code,
                    quarter=quarter,
                    time=time,
                    team=non_null["team"],
                    play=non_null["play"],
                    player_1=non_null['player_1'],
                    player_2=non_null['player_2'],
        #            player_names=non_null["player_names"],
                    player_1_name=non_null['player_1_name'],
                    player_2_name=non_null['player_2_name'],
                    score=score,
                    home_score=home_score,
                    away_score=away_score
                )
                yield item
