import scrapy

from core import db
from core.spiders.sports_reference.base_spider import SRSpider
import string
import bs4
import re

from core.utils import get_player_codes


class PlayersSpider(SRSpider):
    name = "players"

    def parse_page(self, response):
        soup = bs4.BeautifulSoup(response.text)
        players = soup.find(id="players")
        trs = players.find_all("tr")
        for tr in trs[1:]:
            th = tr.find("th")
            href = th.find("a").get("href")
            code = href.split("/")[3].replace(".html", "")
            name = th.text
            tds = tr.find_all("td")
            out = {td.attrs['data-stat']: td.text for td in tds}
            out['code'] = code
            out['hall_of_fame'] = False
            if "*" in name:
                out['hall_of_fame'] = True
                name = name.replace("*", "")
            out['name'] = name
            yield out

    def start_requests(self):
        for letter in string.ascii_lowercase:
            url = self.players_url + letter
            yield scrapy.Request(url=url, callback=self.parse_page)


class PlayerStatsSpider(SRSpider):
    name = "player_stats"

    def __init__(self):
        super().__init__()
        self.player_codes = get_player_codes(start_date = 1900)
        self.season_re = re.compile(r'\d{4,}-\d{2,}')

    def parse_table(self, table):
        if table is None:
            raise Exception("Table is none!")
        out = {}
        trs = table.find_all("tr")
        for tr in trs:
            th = tr.find("th")
            season = th.text
            if self.season_re.match(season) is not None:
                tds = tr.find_all("td")
                tr_data = {td.attrs['data-stat']: td.text for td in tds}
                tr_data['season'] = season
                out[season] = tr_data
        return out

    def parse_stats(self, response):
        specs = db.database_specs['tables']['player_stats']
        code = response.url.split("/")[6].replace('.html', '')
        text = response.text.replace("-->", "").replace("<!--", "")
        soup = bs4.BeautifulSoup(text)
        totals = soup.find(id="all_totals")
        shooting = soup.find(id="shooting")
        salaries = soup.find(id="all_salaries")
        totals_dict = self.parse_table(totals)
        shooting_dict = None
        if shooting is not None:
            shooting_dict = self.parse_table(shooting)
        salaries_dict = None
        if salaries is not None:
            salaries_dict = self.parse_table(salaries)
        seasons = totals_dict.keys()
        for season in seasons:
            out = {}
            out['code'] = code
            out['season'] = season
            out['season_numeric'] = int(season.split('-')[0]) + 1
            out.update(totals_dict[season])
            if shooting_dict is not None:
                if season in shooting_dict.keys():
                    out.update(shooting_dict[season])
            if salaries_dict is not None:
                if season in salaries_dict.keys():
                    out.update(salaries_dict[season])
            out = self.check_dict(out, specs)
            print(out)
            yield out

    def start_requests(self):
        for code in self.player_codes:
            l = code[0]
            url = self.players_url + l + '/' + code + '.html'
            yield scrapy.Request(url=url, callback=self.parse_stats)