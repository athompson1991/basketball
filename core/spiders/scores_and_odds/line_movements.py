# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import scrapy


def make_urls(start, end):
    url_stem = 'https://api.scoresandodds.com/api/scores/scoresandoddsdotcom/home2'
    datetime_start = datetime.strptime(start, '%Y-%m-%d')
    datetime_end = datetime.strptime(end, '%Y-%m-%d')
    delta = datetime_end - datetime_start
    dates = [datetime_start + timedelta(i) for i in range(delta.days)]
    urls = [url_stem + "?gameDate=" + date.strftime("%Y-%m-%d") for date in dates]
    return urls


class LineMovementsSpider(scrapy.Spider):
    name = 'line_movements'
    allowed_domains = ['scoresandodds.com']
    start_urls = make_urls("2018-01-01", "2020-03-01")

    def parse(self, response):
        raw_json = json.loads(response.text)
        active_leagues = raw_json['activeLeagues']
        active_league_games = raw_json['activeLeagueGames']
        for i in range(len(active_leagues)):
            games = active_league_games[i]['games']
            league = active_league_games[i]['league']
            if league == "nba":
                for game in games:
                    id = game['_id']
                    line_moves = game['lineMovements']
                    for move in line_moves:
                        move['league'] = league
                        move['game_id'] = id
                    yield move
