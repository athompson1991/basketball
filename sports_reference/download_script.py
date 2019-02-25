from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
import logging

from sports_reference.spiders.games import GamesSpider
from sports_reference.spiders.playbyplay import PlaybyplaySpider
from scrapy.utils.log import configure_logging

import os

settings = Settings()
os.environ['SCRAPY_SETTINGS_MODULE'] = 'sports_reference.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')


runner = CrawlerRunner()
runner.settings = settings

configure_logging(install_root_handler = False)
logging.basicConfig(
    filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
)

games_spider = GamesSpider()
pbp_spider = PlaybyplaySpider()


runner.crawl(pbp_spider)
runner.crawl(games_spider)
deferred = runner.join()
deferred.addBoth(lambda _: reactor.stop())
reactor.run()

