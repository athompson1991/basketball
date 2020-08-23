import bs4
from nose.tools import assert_equal

from core.spiders.sports_reference.players import PlayerStatsSpider


class TestPlayerStatsSpider:
    dir = "/Users/alex/PycharmProjects/basketball/tests/spiders/html_snippets/"

    def setup(self):
        self.totals = open(self.dir + "totals.html", "r").read()
        self.spider = PlayerStatsSpider()
        self.seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18',
                        '2018-19', '2019-20']
        self.fields = ['age', 'team_id', 'lg_id', 'pos', 'g', 'gs', 'mp', 'fg',
                       'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'fg2',
                       'fg2a', 'fg2_pct', 'efg_pct', 'ft', 'fta', 'ft_pct',
                       'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf',
                       'pts', 'season']

    def test_parse_table(self):
        soup = bs4.BeautifulSoup(self.totals, features="lxml")
        table = self.spider.parse_table(soup)
        assert_equal(self.seasons, list(table.keys()))
        assert_equal(self.fields, list(table['2013-14'].keys()))

    def test_check_dict(self):
        db = {
            'name': {'dtype': 'varchar(100)'},
            'fg': {'dtype': 'integer'},
            'salary': {'dtype': 'varchar(100)'}
        }
        item = {'name': 'Joe Schmo', 'fg': '2000'}
        check = self.spider.check_dict(item, db)
        assert_equal(check, {'name': 'Joe Schmo', 'fg': 2000, 'salary': None})
        item = {'name': 'Joe Schmo', 'fg': '', 'salary': '$1,000'}
        check = self.spider.check_dict(item, db)
        assert_equal(check, {'name': 'Joe Schmo', 'fg': 0, 'salary': '$1,000'})