#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# scraps metadata from Journal of Cognition
#
# (C) 2019 Dominik Lenda, Wroclaw, Poland
# email: dlenda1729@gmail.com
# -----------------------------------------------------------


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


import scrapy
import re
import pandas as pd
import numpy as np
from scrapy.crawler import CrawlerProcess

dataset = pd.read_excel('psyche_science.xlsx')

class PsychScienceSpider_1(scrapy.Spider):
    name = 'psych_science_get_metadata'
    # load from dataset

    def start_requests(self):
        urls = dataset['link']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in response.xpath('//*'):
            yield {
            # title
            'title': response.xpath('normalize-space(.//h1)').get(),
            # 'volume': dataset['volume'],
            # 'issue': dataset['issue'],
            # 'year': dataset['year']
            }






#
# process = CrawlerProcess()
#
# process.crawl(PsychScienceSpider_1)
# process.start()

# dataset.to_excel("psych_science_final.xlsx", encoding = 'utf-8', index = False)
