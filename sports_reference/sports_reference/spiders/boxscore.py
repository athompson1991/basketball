# -*- coding: utf-8 -*-
import scrapy
from ..pipelines import BoxscorePipeline

class BoxscoreSpider(scrapy.Spider):
    name = 'boxscore'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    pipeline = set([BoxscorePipeline])

    def parse(self, response):
        pass

    def start_requests(self):
        pass
