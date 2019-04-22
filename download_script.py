import os
import logging
import argparse

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from sports_reference.spiders.games import GamesSpider
from sports_reference.spiders.playbyplay import PlaybyplaySpider
from sports_reference.spiders.boxscore import BoxscoreSpider
from sports_reference.spiders.shot_chart import ShotChartSpider

def check_directories(target_dir="data"):
    if 'games' not in os.listdir(target_dir):
        os.mkdir(target_dir + "/games")
    if 'pbp' not in os.listdir(target_dir):
        os.mkdir(target_dir + '/pbp')
    if 'boxscore' not in os.listdir(target_dir):
        os.mkdir(target_dir + '/boxscore')
    if 'shotchart' not in os.listdir(target_dir):
        os.mkdir(target_dir + '/shotchart')

def configure():
    temp_settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'sports_reference.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    temp_settings.setmodule(settings_module_path, priority='project')
    return temp_settings

def create_spiders(debug_mode):
    print("Creating spiders...")
    games_spider = GamesSpider
    pbp_spider = PlaybyplaySpider
    boxscore_spider = BoxscoreSpider
    shotchart_spider = ShotChartSpider
    print("Spiders created")
    out = {
        'games': games_spider,
        'pbp': pbp_spider,
        'boxscore': boxscore_spider,
        'shotchart': shotchart_spider
    }
    for k in out.keys():
        out[k].debug = debug_mode
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape basketball-reference")
    parser.add_argument("spiders", help="Get these", type=str, nargs="+", )
    parser.add_argument("--run", help="Run the scrape", action="store_true")
    parser.add_argument("--live", help="Turns off debug mode, pulls all the data", action="store_true")
    args = parser.parse_args()

    check_directories()
    settings = configure()
    runner = CrawlerRunner()
    runner.settings = settings 

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "output")),
            logging.StreamHandler()
        ])

    if args.live:
        print("Running in live mode")
        spiders = create_spiders(debug_mode=False)
    else:
        print("Running in debug mode")
        spiders = create_spiders(debug_mode=True)

    print("Going to run spiders")
    if args.run:
        for spider in args.spiders:
            print("Running spider " + spider)
            runner.crawl(spiders[spider])

        deferred = runner.join()
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
