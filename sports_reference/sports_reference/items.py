# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SportsReferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GameItem(scrapy.Item):
    code = scrapy.Field()
    start_time = scrapy.Field()
    home_team = scrapy.Field()
    visiting_team = scrapy.Field()

class PlaybyplayItem(scrapy.Item):
    code = scrapy.Field()
    time = scrapy.Field()