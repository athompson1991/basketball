import scrapy
from .base_spider import SRSpider
from ..constants import BASKETBALL_REFERENCE_URL
from ..items import ShotChartItem
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
        code = response.url
        scorebox = response.css('div.scorebox')
        soup = bs4.BeautifulSoup(scorebox[0].extract())
        teams = soup.find_all('strong')
        home_href = teams[0].find_all('a', href=True)[0]['href']
        visit_href = teams[1].find_all('a', href=True)[0]['href']

        home_team = home_href.split("/")[2]
        visiting_team = visit_href.split("/")[2]
        row = ShotChartItem(
            code=code,
            home_team=home_team,
            visiting_team=visiting_team
        )
        return row



