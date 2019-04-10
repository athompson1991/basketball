import os
import logging

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from sports_reference.spiders.games import GamesSpider
from sports_reference.spiders.playbyplay import PlaybyplaySpider
from sports_reference.spiders.boxscore import BoxscoreSpider

def check_directories():
    if 'games' not in os.listdir():
        os.mkdir("games")
    if 'pbp' not in os.listdir():
        os.mkdir('pbp')
    if 'boxscore' not in os.listdir():
        os.mkdir('boxscore')

def configure():
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'sports_reference.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    return settings

def create_spiders(debug=True):
    PlaybyplaySpider.DEBUG = debug

    games_spider = GamesSpider()
    pbp_spider = PlaybyplaySpider()
    boxscore_spider = BoxscoreSpider()
    out = [games_spider, pbp_spider, boxscore_spider]
    return out



if __name__ == "__main__":
    check_directories()
    SETTINGS = configure()

    runner = CrawlerRunner()
    runner.settings = SETTINGS

    configure_logging(install_root_handler = False)
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "output")),
            logging.StreamHandler()
        ])

    spiders = create_spiders(True) # Put false to run all games - USE AT YOUR OWN RISK

    for spider in spiders:
        runner.crawl(spider)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
