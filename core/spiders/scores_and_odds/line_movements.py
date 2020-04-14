# -*- coding: utf-8 -*-
import json
import scrapy

from core.utils import generate_dates

url_stem = 'https://api.scoresandodds.com/api/scores/scoresandoddsdotcom/home2'

class LineMovementsSpider(scrapy.Spider):
    name = 'line_movements'
    allowed_domains = ['scoresandodds.com']
    dates = generate_dates("2018-06-01", "2020-01-01")
    start_urls = [url_stem + "?gameDate=" + date.strftime("%Y-%m-%d") for date in dates]

    def parse(self, response):
        raw_json = json.loads(response.text)
        active_league_games = {i['league']:i for i in raw_json['activeLeagueGames']}
        if 'nba' in active_league_games.keys():
            games = active_league_games['nba']['games']
            for game in games:
                key = game['gamePrimaryId']
                game_date = game['gameDateTime']
                home_team = game['homeTeam']['location'] + ' ' + game['homeTeam']['nickname']
                away_team = game['awayTeam']['location'] + ' ' + game['awayTeam']['nickname']
                money_line = game['lineBetFormatted']['moneyLine']
                out = {
                    'key': key,
                    'date_timestamp': game_date,
                    'date_url': response.url.split("=")[1],
                    'home_team': home_team,
                    'away_team': away_team,
                    **money_line
                }
                yield out
