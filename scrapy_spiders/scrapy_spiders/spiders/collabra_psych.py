# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
import re
from scrapy_spiders.items import CollabraPsychMetadata
from scrapy.loader import ItemLoader
# from bs4 import BeautifulSoup



HOME = 'https://www.collabra.org'

class CollabraPsychSpider(scrapy.Spider):
    name = 'collabra_psych'
    allowed_domains = ['collabra.org']
    start_urls = (
    HOME,
    )
    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title', 'publication_year', 'article_type', 'volume',
    'issue', 'doi', 'abstract', 'keywords', 'url', 'pdf_url_download',
    'peer_review_url', 'conflict_of_interests', 'acknowledgements',
    'data_acessibility', 'data_accessibility_links', 'funding_info', 'author_contributions',
    'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs'],
    }
    #
    # def start_requests(self):
    #     start_urls = HOME
    #     # for url in start_urls:
    #         yield scrapy.Request(url = url, callback = self.parse_home)
#
    def parse(self, response):
        # l = ItemLoader(item=CollabraPsychMetadata(), response=response)
        # l.add_xpath('title', '//*[@itemprop="name"][1]/tex

        issue = response.xpath('//li/a[contains(text(), "Issue Archive")]\
# /@href').get()
        archive_url = f'{HOME}{issue}'
#         yield scrapy.Request(url = archive_url, callback = self.parse_archive)
#
#     def parse_archive(self, response):
#         volume_urls = response.css('div[class = "volume-caption volume-\
# caption-large"] a::attr(href)')
#         for url in volume_urls:
#             full_url = f'{HOME}{url.get()}'
#             yield scrapy.Request(url = full_url, callback = self.parse_volume)
#
#     def parse_volume(self, response):
#         item = CollabraPsychMetadata()
#         article_urls = response.css('div[class = "caption-text"] a::attr(href)')
#
#         vol_issue_url = response.request.url
#         item['volume'] = re.search("volume/(\d+)", vol_issue_url).group(1)
#         item['issue'] = re.search("issue/(\d+)", vol_issue_url).group(1)
#
#         for url in article_urls:
#         # some of article_urls include links to "collections";
#         # avoid these links because they do not directly lead to the article
#             if bool(re.search("collection", url.get())):
#                 continue
#             full_url = f'{HOME}{url.get()}'
#             request = scrapy.Request(url = full_url, callback = self.parse_article)
#             request.meta['item'] = item
#             yield request
#
#     def parse_article(self, response):
#         def get_url(section_title):
#             select_link = response.xpath(f'//div/h2[contains(text(), "{section_title}")]/following-sibling::*/a')
#             if select_link != []:
#                 return select_link.xpath('./@href').get()
#             else:
#                 return 'NA'
#
#         item = response.meta['item']
#
#         item['title'] = response.xpath('normalize-space(//div[@class="article-title"]/h1)').get()
#         year  = response.xpath('normalize-space(//div[@class="credit-block credit-separator"])').get()
#         item['publication_year'] = re.search("\d{4}$", year).group(0)
#         item['article_type'] = response.xpath('normalize-space(//div[@class="article-title"]/h4)').get()
#         item['doi'] = response.xpath('//div[@class="authors"]/span[@class="span-citation"]/a/text()').get()
#         item['abstract'] = response.xpath('normalize-space(//h2[@id="abstract"]/following-sibling::p)').getall()
#         item['url'] = response.request.url
#         item['peer_review_url'] = get_url("Peer Review")
#         item['data_accessibility_links'] = get_url("Data Accessibility")
#
#
#         return item
#
# # # # 'abstract', 'keywords', 'url', 'pdf_url_download',
# # # # 'peer_rev_url', 'conflict_of_interests', 'acknowledgements',
# # # # 'data_acessibility', 'data_links', 'funding_info', 'author_contributions',
# # # # 'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs']
