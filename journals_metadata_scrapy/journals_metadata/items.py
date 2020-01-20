# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 3. Psychological Science: all articles since badges started in 2014 that have an
# "Open Practices" statement, i.e., starting at Volume 25 Issue 5, May 2014
# (though only 1 article in that issue); 0 in next issue; 6 articles in Issue 7)
# (at least 2 badges)
#  Metadata to extract (from PDF and HTML):
# • title, year, DOI, article type (don't think this is available), abstract text,
# "Keywords", # of downloads (from an article's "metrics" subpage; example),
# "Declaration of Conflicting Interests", article HTML URL (only if open access),
# article PDF URL (sci-hub URL), "Open Practices" statement (extract all URLs and
# save in open.content.URLs field), "Funding", and "Authors Contributions".

class Psych_Science_Metadata(scrapy.Item):
    # title = scrapy.Field()
    # year = scrapy.Field()
    # volume = scrapy.Field()
    # issue = scrapy.Field()
    doi = scrapy.Field()
    # abstract = scrapy.Field()
    # keywords = scrapy.Field()
    # url = scrapy.Field()
    # pdf_url = scrapy.Field()
    # conflict_of_interests = scrapy.Field()
    # funding = scrapy.Field()
    # open_practices = scrapy.Field()
    # acknowledgements = scrapy.Field()
    altmetrics = scrapy.Field()
    # last_updated = scrapy.Field(serializer=str)
