import scrapy
import bs4

from core.spiders.sports_reference.base_spider import SRSpider


class TeamsSpider(SRSpider):
    name = "teams"

    def __init__(self):
        self.url_stem = "https://www.basketball-reference.com/teams/"
        self.codes = self.get_codes()
        self.urls = [self.url_stem + code + '/' for code in self.codes]

    def parse_item(self, response):
        out = {}
        out['code'] = response.url.split('/')[4]
        soup = bs4.BeautifulSoup(response.text)
        alt_codes = self.parse_alt_codes(soup, out['code'])
        info = soup.find(id="info")
        team = info.find_all('div')[0].find('h1').text.replace('\n', '')
        p = info.find_all('p')
        location = p[2].text.replace('\n', '').replace('Location:  ', '')
        out['alt_codes'] = str(alt_codes)
        out['location'] = location
        out['team_name'] = team
        return out

    def parse_alt_codes(self, soup, main_code):
        out = set()
        table = soup.find(id=main_code)
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) > 0:
                code = tds[1].find("a").get("href")
                out.add(code.split("/")[2])
        return out

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_item)


class TeamsDetailSpider(TeamsSpider):

    name = "teams_detail"

    def parse_detail(self, response):
        url_code = response.url.split('/')[4]
        soup = bs4.BeautifulSoup(response.text)
        table = soup.find(id=url_code)
        trs = table.find_all("tr")
        for tr in trs[1:]:
            season = tr.find('th').text
            tds = tr.find_all("td")
            data = {td.attrs['data-stat']: td.text for td in tds}
            code = tds[1].find('a').get('href').split("/")[2]
            data['season'] = season
            data['url_code'] = url_code
            data['code'] = code
            yield data

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse_detail)