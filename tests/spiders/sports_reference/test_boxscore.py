from nose.tools import assert_equal

from core.spiders.sports_reference.boxscore import BoxscoreSpider
from tests.spiders.sports_reference.fake_response import fake_response

import os

class TestBoxscore:

    def setup(self):
        self.test_dir = "/Users/alex/PycharmProjects/basketball/tests/spiders/html_snippets/boxscore.html"
        self.spider = BoxscoreSpider()
        self.fake_response = fake_response(
            self.test_dir,
            url="https://www.basketball-reference.com/boxscores/201810160GSW.html"
        )

    def test_parse(self):
        results = self.spider.parse(self.fake_response)
        result = next(results)
        assert_equal(result['code'], '201810160GSW')
