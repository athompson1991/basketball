from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
import logging

from sports_reference.spiders.games import GamesSpider
from sports_reference.spiders.playbyplay import PlaybyplaySpider
from sports_reference.spiders.boxscore import BoxscoreSpider
from scrapy.utils.log import configure_logging

import os

settings = Settings()
os.environ['SCRAPY_SETTINGS_MODULE'] = 'sports_reference.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')

if 'games' not in os.listdir():
    os.mkdir("games")
if 'pbp' not in os.listdir():
    os.mkdir('pbp')
if 'boxscore' not in os.listdir():
    os.mkdir('boxscore')

runner = CrawlerRunner()
runner.settings = settings

configure_logging(install_root_handler = False)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(".", "output")),
        logging.StreamHandler()
    ])

games_spider = GamesSpider()
PlaybyplaySpider.DEBUG = True # Put false to run all games - USE AT YOUR OWN RISK
pbp_spider = PlaybyplaySpider()
boxscore_spider = BoxscoreSpider()

runner.crawl(pbp_spider)
runner.crawl(games_spider)
runner.crawl(boxscore_spider)

deferred = runner.join()
deferred.addBoth(lambda _: reactor.stop())
reactor.run()
