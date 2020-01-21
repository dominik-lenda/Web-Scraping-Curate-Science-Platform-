# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PsychScienceMetadata(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    doi = scrapy.Field()
    abstract = scrapy.Field()
    article_type = scrapy.Field()
    keywords = scrapy.Field()
    url = scrapy.Field()
    pdf_url = scrapy.Field()
    conflict_of_interests = scrapy.Field()
    author_contributions = scrapy.Field()
    funding = scrapy.Field()
    open_practices = scrapy.Field()
    acknowledgements = scrapy.Field()
    altmetrics_score = scrapy.Field()
    altmetrics_total_outputs = scrapy.Field()
