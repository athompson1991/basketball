# -*- coding: utf-8 -*-

BOT_NAME = 'sports_reference'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sports_reference (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'sports_reference.pipelines.CSVPipeline': 300,
}

