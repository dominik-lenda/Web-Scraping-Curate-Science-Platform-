# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy_spiders.items import CollabraMetadata
import re
from scrapy.loader import ItemLoader


HOME = 'https://www.collabra.org'

class CollabraSpider(scrapy.Spider):
    name = 'collabra'
    # allowed_domains = ['collabra']
    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title', 'publication_year', 'article_type', 'volume',
    'issue', 'doi', 'abstract', 'keywords', 'url', 'pdf_url_download',
    'peer_review_url', 'conflict_of_interests', 'acknowledgements',
    'data_acessibility', 'data_accessibility_links', 'funding_info', 'author_contributions',
    'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs'],
    }


    def start_requests(self):
        start_urls = ["https://www.collabra.org/6/volume/6/issue/1/",]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_article_list)


    def parse_article_list(self, response):
        print(response.xpath('//li[@class = "article-block"]'))
        print(len(response.xpath('//li[@class = "article-block"]')))































    # def parse_main(self, response):
    #     article_block = response.xpath('//div[@class="article-actions"]')
    #     for article in article_block:
    #         # vol_is_url = article.xpath('normalize-space(./div[@class="aside"]/a/@href)').get()
    #         # item['volume'] = re.search("volume/(\d+)", vol_is_url).group(1)
    #         # item['issue'] = re.search("issue/(\d+)", vol_is_url).group(1)
    #         article_url = f"{HOME}{article.xpath('./a/@href').get()}"
    #         # item['url'] = article_url
    #         # request = scrapy.Request(url = article_url, callback = self.parse_article)
    #         # request.meta['item'] = item
    #         # yield request
    #         print(article_url)

    # def parse_article(self, response):
        # def get_url(section_title):
        #     select_link = response.xpath(f'//div/h2[contains(text(), "{section_title}")]/following-sibling::*/a')
        #     if select_link != []:
        #         return select_link.xpath('./@href').get()
        #     else:
        #         return 'NA'
        # #
        # item = response.meta['item']
        #
        # yield{
        # 'title':response.xpath('normalize-space(//div[@class="article-title"]/h1)').get(),
        # }
        #
        # return item







        # wszystkie linki na stronie
        # response.xpath('//a[contains(@href, "volume")]')

        # 1. parse data for each article
        # 2. jump to the articles extract data
        # 3. get new data

        # response.xpath('//*[contains(@class,"active")]')
        # item = CollabraMetadata()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
