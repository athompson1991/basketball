# -*- coding: utf-8 -*-

BOT_NAME = 'basketballbot'

SPIDER_MODULES = ['core.spiders.scores_and_odds', 'core.spiders.sports_reference']
NEWSPIDER_MODULE = 'core.spiders'

ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'core.pipelines.CSVPipeline': 300,
}

