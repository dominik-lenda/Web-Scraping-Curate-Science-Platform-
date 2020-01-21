# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response

HOME = 'https://www.collabra.org'

class CollabraPsychSpider(scrapy.Spider):
    name = 'collabra_psych'

    def start_requests(self):
        start_urls = [HOME]
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse_home)

    def parse_home(self, response):
        issue = response.xpath('//li/a[contains(text(), "Issue Archive")]\
/@href').get()
        archive_url = f'{HOME}{issue}'
        yield scrapy.Request(url = archive_url, callback = self.parse_archive)

    def parse_archive(self, response):
        volume_urls = response.css('div[class = "volume-caption volume-\
caption-large"] a::attr(href)')
        for url in volume_urls:
            full_url = f'{HOME}{url.get()}'
            yield scrapy.Request(url = full_url, callback = self.parse_volume)

# remove collections; if articles or sth
    def parse_volume(self, response):
        article_urls = response.css('div[class = "caption-text"] a::attr(href)')
        for url in article_urls:
            full_url = f'{HOME}{url.get()}'
            yield scrapy.Request(url = full_url, callback = self.parse_article)


    def parse_article(self, response):
        title = response.css('div[class="article-title"] h1::text').get()
        yield{
        'title': title
        }
