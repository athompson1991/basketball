BOT_NAME = 'basketballbot'

SPIDER_MODULES = [
    'core.spiders.scores_and_odds',
    'core.spiders.sports_reference',
    'core.spiders.sportsbook_review'
]

NEWSPIDER_MODULE = 'core.spiders'

ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    # 'core.pipelines.PostgresPipeline': 400,
    'core.pipelines.CSVPipeline': 300
}

SEASONS = list(range(2000, 2020))
CODES_FILTER = '2000-01-01'

AUTOTHROTTLE_ENABLED = True

OUTPUT_DIRECTORY = "data"
