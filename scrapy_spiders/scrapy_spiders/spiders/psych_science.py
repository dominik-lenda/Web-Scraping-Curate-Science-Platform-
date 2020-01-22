# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.shell import inspect_response
from scrapy_spiders.items import PsychScienceMetadata
from scrapy.loader import ItemLoader
import json

# 3. Psychological Science: all articles since badges started in 2014 that have an
# "Open Practices" statement, i.e., starting at Volume 25 Issue 5, May 2014
# (though only 1 article in that issue); 0 in next issue; 6 articles in Issue 7)
# (at least 2 badges)
#  Metadata to extract (from PDF and HTML):
# • title, year, DOI, article type (don't think this is available), abstract text,
# "Keywords", # of downloads (from an article's "metrics" subpage; example),
# "Declaration of Conflicting Interests", article HTML URL (only if open access),
# article PDF URL (sci-hub URL), "Open Practices" statement (extract all URLs and
# save in open.content.URLs field), "Funding", and "Authors Contributions",
# number of views, number of downloads

HOME = "https://journals.sagepub.com"

class PsychScienceSpider(scrapy.Spider):
    name = 'psych_science'

    custom_settings = {
    'FEED_EXPORT_FIELDS' : ['title', 'year', 'volume', 'issue', 'doi',
    'article_type', 'abstract', 'article_type', 'keywords', 'url', 'pdf_url',
    'conflict_of_interests', 'author_contributions', 'funding', 'open_practices',
    'acknowledgements', 'altmetrics_score', 'altmetrics_total_outputs'],
    }

    def start_requests(self):
        start_urls = ['https://journals.sagepub.com/loi/PSS?year=2010-2019']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_year)


    def parse_year(self, response):
        all_years = response.css('h4 a')
        for year in all_years:
            if int(year.css('::text').get()) >= 2014:
                url_year = f"{HOME}{year.css('::attr(href)').get()}"
                yield scrapy.Request(url_year, callback=self.parse_volumes)

    def parse_volumes(self, response):
        all_issues = response.css('h6 a')
        for issue in all_issues:
            issue_url = issue.css('::attr(href)').get()
            yield scrapy.Request(issue_url, callback = self.parse_issue)

    def parse_issue(self, response):
        """Get articles with at least two badges: open data and open material, or
        open data and preregistration, or open material and preregistration.
        """

        for article in response.css('tr'):
            access = article.css('.accessIconContainer div').xpath('./img/@alt').get()
            if (access != "No Access" and access != None):
                badge = article.css('.accessIconContainer').xpath('./following-sibling::td[@valign="top"]/div[@class = "tocDeliverFormatsLinks"]')
                open_data = badge.css('img[class="openData"]')
                open_material = badge.css('img[class="openMaterial"]')
                prereg = badge.css('img[class="preregistration"]')
                if ((open_data != [] and open_material != []) or
                (open_data != [] and prereg != []) or
                (open_material != [] and prereg != [])):
                    path = './td[@valign="top"]/div/a[@data-item-name="click-article-title"]/@href'
                    open_article_url = f'{HOME}{article.xpath(path).get()}'
                    yield scrapy.Request(open_article_url, callback = self.parse_article)


    def parse_article(self, response):
        def extract_data(title):
            p_tags_values = []
            for p_tag in response.xpath('//span[@class="NLM_fn"]'):
                # check if any of elements is NA, allows to save clear data
                p_tags_values.append(p_tag.xpath(f'./p/span[contains(text(), "{title}")]').get())
                show_NA = [element != None for element in p_tags_values]
            bool = any(show_NA)
            if bool == True:
                for p_tag in response.xpath('//span[@class="NLM_fn"]'):
                    if p_tag.xpath(f'./p/span[contains(text(), "{title}")]').get() != None:
                        full_text_list = p_tag.xpath('descendant-or-self::*/text()').getall()
                        full_text = ''.join(full_text_list[1::]).strip()
                return full_text
            else:
                return "NA"


        def get_info_or_NA(query):
            if response.xpath(query).get() != '':
                return response.xpath(query).get()
            else:
                return "NA"

        item = PsychScienceMetadata()

        vol_issue_year = response.css('div[class="tocLink"] a::text').get()
        doi = response.css('a[class="doiWidgetLink"]::text').get()
        extract_data("Author Contribution")
        item['title'] = response.xpath('normalize-space(//h1)').get()
        item['volume'] = re.search("Vol(.\d+)", vol_issue_year).group(1).strip()
        item['issue'] = re.search("Issue(.\d+)", vol_issue_year).group(1).strip()
        item['year'] =  re.search("\d{4}$", vol_issue_year).group(0)
        item['doi'] = doi
        item['article_type'] = get_info_or_NA('//span[@class = "ArticleType"]/span/text()')
        item['abstract'] = response.xpath('normalize-space(//*[@class="abstractSection abstractInFull"]/p)').getall()[0]
        item['keywords'] = ', '.join(response.css('kwd-group a::text').getall())
        item['url'] = response.request.url
        item['pdf_url'] = f"""{HOME}{response.css('a[data-item-name="download-PDF"]::attr(href)').get()}"""
        item['acknowledgements'] = get_info_or_NA('normalize-space(//div[@class="acknowledgement"]/p)')
        item['author_contributions'] = extract_data("Author Contribution")
        item['conflict_of_interests'] = extract_data("Declaration of Conflicting Interests")
        item['funding'] = extract_data("Funding")
        item['open_practices'] = extract_data("Open Practice")

        api_altmetric_home = "https://api.altmetric.com/v1/doi/"
        altmetric_urls = f'{api_altmetric_home}{re.sub("https://doi.org/", "", doi)}'
        request = scrapy.Request(altmetric_urls, callback = self.parse_altmetrics)
        request.meta['item'] = item
        yield request

    def parse_altmetrics(self, response):
        item = response.meta["item"]
        dictionary_txt = response.css('p::text').get()
        d = json.loads(dictionary_txt)
        item['altmetrics_score'] = d['score']
        item['altmetrics_total_outputs'] = d['context']['all']['count']
        return item
