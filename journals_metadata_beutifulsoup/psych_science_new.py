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

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
