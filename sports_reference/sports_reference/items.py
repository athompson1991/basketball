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
    home_code = scrapy.Field()
    home_points = scrapy.Field()
    visiting_team = scrapy.Field()
    visiting_code = scrapy.Field()
    visitor_points = scrapy.Field()
    has_ot = scrapy.Field()
    attendance = scrapy.Field()

class PlaybyplayItem(scrapy.Item):
    code = scrapy.Field()
    quarter = scrapy.Field()
    time = scrapy.Field()
    team = scrapy.Field()
    player_codes = scrapy.Field()
    player_names = scrapy.Field()
    score = scrapy.Field()
    play = scrapy.Field()