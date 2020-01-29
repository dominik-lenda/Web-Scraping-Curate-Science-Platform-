# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
import re
from scrapy_spiders.items import CollabraMetadata
# from scrapy.loader import ItemLoader


HOME = 'https://www.collabra.org'

class CollabraPsychSpider(scrapy.Spider):
    name = 'collabra_psych'

    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title', 'publication_year', 'article_type', 'volume',
    'issue', 'doi', 'abstract', 'keywords', 'url', 'pdf_url_download',
    'peer_review_url', 'conflict_of_interests', 'acknowledgements',
    'data_acessibility', 'data_accessibility_links', 'funding_info', 'author_contributions',
    'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs'],
    }

    def start_requests(self):
        start_urls = ['https://www.collabra.org/issue/archive']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):
        volume_urls = response.css('div[class = "volume-caption volume-\
caption-large"] a::attr(href)')
        for url in volume_urls:
            full_url = f'{HOME}{url.get()}'
            yield scrapy.Request(url = full_url, callback = self.parse_volume)

    def parse_volume(self, response):
        # response.xpath('//div[@class = "icon-with-list"]//a[contains(text(), "XML")]')
        for article in response.xpath('//div[@class="article-actions"]'):
            item = CollabraMetadata()
            item['url'] = f"{HOME}{article.xpath('./a/@href').get()}"
            vol_issue_url = response.request.url
            item['volume'] = re.search("volume/(\d+)", vol_issue_url).group(1)
            item['issue'] = re.search("issue/(\d+)", vol_issue_url).group(1)

            # extract XML and PDF links
            xml_pdf = article.xpath('.//div[@class = "icon-with-list"]')
        # for xml_pdf in response.xpath('//div[@class = "icon-with-list"]'):

            xml = xml_pdf.xpath('normalize-space(.//a[contains(text(), "XML")]/@href)').get()
            full_xml = f'{HOME}{xml}'
            pdf = xml_pdf.xpath('normalize-space(.//a[contains(text(), "PDF")]/@href)').get()
            full_pdf_url = f'{HOME}{pdf}'
            item['pdf_url_download'] = full_pdf_url

            # meta - pass item to the next method
            yield scrapy.Request(url = full_xml, callback = self.parse_article_xml, meta={'item': item})

        # for url in article_urls:
        #     item = CollabraMetadata()
        #     vol_issue_url = response.request.url
        #     item['volume'] = re.search("volume/(\d+)", vol_issue_url).group(1)
        #     item['issue'] = re.search("issue/(\d+)", vol_issue_url).group(1)
        #     full_url = f'{HOME}{url.get()}'
        #     yield scrapy.Request(url = full_url, callback = self.parse_article, meta={'item': item})

    def parse_article_xml(self, response):

        def get_url(tag, title):
            content = response.xpath(f'//{tag}[contains(translate(.,\
 "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]')

            if content.xpath('.//ext-link').get() != None:
                url = content.xpath('normalize-space(.//ext-link)').get()
            elif content.xpath('.//uri').get() != None:
                url = content.xpath('normalize-space(.//uri)').get()
            else:
                url = 'NA'
            return url

        def get_text_short(xpath):
            text = response.xpath(f'normalize-space({xpath})').get()
            return "NA" if not text else text



# response.xpath('//title[contains(text(), "Data Access")]/parent::sec').get()

        def get_text_long(tag, *title):
            xpath = f'normalize-space(//title[contains(translate(. ,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}") or\
contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "{title}")]/parent::{tag})'
            content = response.xpath(xpath).get()
            if content != '':
                return content
            else:
                return 'NA'


        def get_text_long(tag, *titles):
            for title in titles:
                xpath = f'//title[contains(translate(. ,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]'
                text = response.xpath(f'normalize-space({xpath}/parent::{tag})').get()
                return "NA" if not text else text

        item = response.meta['item']


        item['title'] = get_text_short('//article-title')
        item['article_type'] = get_text_short('//subject')
        item['publication_year'] = get_text_short('//pub-date/year')
        item['doi'] = get_text_short('//article-id')
        item['abstract'] = get_text_short('//abstract')
        keywords = ', '.join(response.xpath('//kwd/text()').getall())
        item['keywords'] = keywords if keywords else "NA" # empty string is False
        item['peer_review_url'] = get_url('sec', 'peer review comments')
        item['data_accessibility_statement'] = get_text_long('sec', 'data accessibility')


        # 'conflict_of_interests', 'acknowledgements',
        # # # # # 'data_acessibility', 'data_links', 'funding_info', 'author_contributions'















        return item





        # item['title'] = response.xpath('normalize-space(//div[@class="article-title"]/h1)').get()
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
# 'conflict_of_interests', 'acknowledgements',
# # # # # 'data_acessibility', 'data_links', 'funding_info', 'author_contributions',
# # # # # 'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs']
