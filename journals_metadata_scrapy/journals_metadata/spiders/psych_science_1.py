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

# load from dataset
dataset = pd.read_excel('psyche_science.xlsx')

class PsychScienceSpider(scrapy.Spider):
    name = 'psych_science_get_metadata'

    def start_requests(self):
        urls = dataset['link']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # get title
        title = response.xpath('normalize-space(.//h1)').get()





        # scrap open_access articles with at least 2 badges
        for article in response.css('tr'):
            access = article.css('.accessIconContainer div').xpath('./img/@alt').get()
            if access != "No Access" and access != None:
                badge = article.css('.accessIconContainer').xpath('./following-sibling::td[@valign="top"]/div[@class = "tocDeliverFormatsLinks"]')
                open_data = badge.css('img[class="openData"]')
                open_material = badge.css('img[class="openMaterial"]')
                prereg = badge.css('img[class="preregistration"]')
                if ((open_data != [] and open_material != []) or
                (open_data != [] and prereg != []) or
                (open_material != [] and prereg != [])):
                    vol_issue = response.css('div[class="journalNavTitle"]::text').get()
                    link = f"{HOME}{badge.css('a::attr(href)').get()}"
                    yield {
                    'access': access,
                    'link' : link,
                    'vol_issue' : vol_issue.strip()
                    }
