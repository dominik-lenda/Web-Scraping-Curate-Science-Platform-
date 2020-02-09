# -*- coding: utf-8 -*-
import scrapy
import re


HOME = "https://journals.sagepub.com"


class PsychScienceSpider(scrapy.Spider):
    name = 'psy_sci_stats'

    # custom_settings = {
    # 'FEED_EXPORT_FIELDS' : ['title', 'year', 'volume', 'issue', 'doi',
    # 'article_type', 'abstract', 'article_type', 'keywords', 'url', 'pdf_url',
    # 'conflict_of_interests', 'author_contributions', 'funding', 'open_practices',
    # 'acknowledgements', 'altmetrics_score', 'altmetrics_total_outputs'],
    # }

    def start_requests(self):
        start_urls = ['https://journals.sagepub.com/loi/PSS?year=2010-2019']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_year)


    def parse_year(self, response):
        all_years = response.css('h4 a')
        for year in all_years:
            if int(year.css('::text').get()) >= 2010:
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
        year = response.xpath('//div[@class="journalNavTitle"]/text()').get()
        year1 = re.search("\d{4}$", year).group(0)
        for article in response.css('tr'):
            access = article.xpath('.//*[@class ="accessIconContainer"]//img/@title').get()
            access_bool = 0 if access == "No Access" else 1

            if access != None:

                badges = article.xpath('.//div[@class = "tocDeliverFormatsLinks"]')
                open_data_l = badges.css('img[class="openData"]')
                open_materials_l = badges.css('img[class="openMaterial"]')
                prereg_l = badges.css('img[class="preregistration"]')

                open_data = 1 if open_data_l != [] else 0
                open_materials = 1 if open_materials_l != [] else 0
                prereg = 1 if prereg_l != [] else 0



                yield {
                "access" : access,
                "access_bool": access_bool,
                "open_data": open_data,
                "open_materials" : open_materials,
                "preregistration": prereg,
                "year": year1,
                "url" : response.url,
                }
