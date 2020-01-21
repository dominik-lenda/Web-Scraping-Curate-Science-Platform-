# -*- coding: utf-8 -*-
import scrapy


class CollabraPsychSpider(scrapy.Spider):
    name = 'collabra_psych'
    allowed_domains = ['collabra.org']
    start_urls = ['http://collabra.org/']

    def parse(self, response):
        pass
