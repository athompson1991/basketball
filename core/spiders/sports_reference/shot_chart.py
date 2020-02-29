import scrapy
import re
from .base_spider import SRSpider
from core.constants import BASKETBALL_REFERENCE_URL
from core.items import ShotChartItem
import bs4

class ShotChartSpider(SRSpider):
    name = 'shotchart'

    def __init__(self):
        super().__init__()
        self.configure()
        self.codes = self.config['shotchart']['codes']

    def start_requests(self):
        url_stem = BASKETBALL_REFERENCE_URL + "boxscores/shot-chart/"
        urls = [url_stem + code + ".html" for code in self.codes]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url_ls = response.url.split('/')
        code = url_ls[len(url_ls) - 1][:-5]

        home_team, visiting_team = self.get_team_codes(response)

        home_wrapper = response.css('div#wrapper-' + home_team).css('div#shots-' + home_team)
        visitor_wrapper = response.css('div#wrapper-' + visiting_team).css('div#shots-' + visiting_team)

        shots_soup = bs4.BeautifulSoup(home_wrapper[0].extract())
        divs = shots_soup.find_all('div')

        for div in divs[1:]:
            div_contents = self.parse_div(div)
            row = ShotChartItem(
                code=code,
                team=home_team,
                team_type='home',
                shot_location=div_contents['shot_location'],
                x=div_contents['x'],
                y=div_contents['y'],
                made_shot=div_contents['made_shot'],
                tip=div_contents['tip'],
                player_code=div_contents['player_code'],
                quarter=div_contents['quarter'],
                time_left=div_contents['time_left']
            )
            yield row

        shots_soup = bs4.BeautifulSoup(visitor_wrapper[0].extract())
        divs = shots_soup.find_all('div')

        for div in divs[1:]:
            div_contents = self.parse_div(div)
            row = ShotChartItem(
                code=code,
                team=visiting_team,
                team_type='visitor',
                shot_location=div_contents['shot_location'],
                x=div_contents['x'],
                y=div_contents['y'],
                made_shot=div_contents['made_shot'],
                tip=div_contents['tip'],
                player_code=div_contents['player_code'],
                quarter=div_contents['quarter'],
                time_left=div_contents['time_left']
            )
            yield row

    def parse_div(self, div):
        shot_location = div.attrs['style']
        split_shot_location = re.findall(r'\d+', shot_location)

        x = split_shot_location[1]
        y = split_shot_location[0]

        if div.text == '●':
            made_shot = True
        elif div.text == '×':
            made_shot = False
        else:
            made_shot = "NA"

        tip = div.attrs['tip']
        time_left = re.findall(r'\d+:\d+\.\d+', tip)[0]

        data_ls = div.attrs['class']
        quarter = data_ls[1]
        player_code = data_ls[2]

        out = {
            "shot_location": shot_location,
            "x": x,
            "y": y,
            "made_shot": made_shot,
            "tip": tip,
            "time_left": time_left,
            "quarter": quarter,
            "player_code": player_code
        }

        return out

