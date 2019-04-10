# -*- coding: utf-8 -*-
import re
from datetime import  datetime, timedelta
import json
import scrapy
import bs4

def make_urls(start, end):
    url_stem = 'http://scoresandodds.com/gameDate/'
    datetime_start = datetime.strptime(start, '%Y-%m-%d')
    datetime_end = datetime.strptime(end, '%Y-%m-%d')
    delta = datetime_end - datetime_start
    dates = [datetime_start + timedelta(i) for i in range(delta.days)]
    urls = [url_stem + date.strftime("%Y-%m-%d") + "/" for date in dates]
    return urls


class LineMovementsSpider(scrapy.Spider):
    name = 'line_movements'
    allowed_domains = ['scoresandodds.com']
    start_urls = make_urls("2019-01-01", "2019-03-01")

    def parse(self, response):
        data = response.css("script")[5].extract()
        soup = bs4.BeautifulSoup(data)
        js_vars = soup.text.split(";")
        betting_var = js_vars[0]
        json_str = re.findall(r"\{.+\}", betting_var)[0]
        games_json = json.loads(json_str)
        for league in games_json['activeLeagueGames']:
            if league['title'] == 'NBA':
                games = league['games']
        for game in games:
            home_team = game['homeTeamName']
            away_team = game['awayTeamName']
            game_id = game['gamePrimaryId']
            game_datetime = game['gameDateTime']
            line_movements = game['lineMovements']
            for line in line_movements:
                yield {
                    'scrape_id': line['_id'],
                    'game_id': game_id,
                    'game_datetime': game_datetime,
                    'home': home_team,
                    'away': away_team,
                    'timestamp': line['changeAt'],
                    'favorite': line['favorite'],
                    'favorite_money': line['favoriteMoney'],
                    'favorite_points': line['favoritePts'],
                    'home_money_line': line['homeMoneyLine'],
                    'away_money_line': line['awayMoneyLine'],
                    'total': line['total']
                }



