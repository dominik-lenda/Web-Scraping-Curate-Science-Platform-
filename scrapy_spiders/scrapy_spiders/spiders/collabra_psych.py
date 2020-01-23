# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
import re
from scrapy_spiders.items import CollabraPsychMetadata
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup



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
        start_urls = [HOME]
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse_home)

    def parse_home(self, response):
        issue = response.xpath('//li/a[contains(text(), "Issue Archive")]\
/@href').get()
        archive_url = f'{HOME}{issue}'
        yield scrapy.Request(url = archive_url, callback = self.parse_archive)

    def parse_archive(self, response):
        volume_urls = response.css('div[class = "volume-caption volume-\
caption-large"] a::attr(href)')
        for url in volume_urls:
            full_url = f'{HOME}{url.get()}'
            yield scrapy.Request(url = full_url, callback = self.parse_volume)

    def parse_volume(self, response):
        item = CollabraPsychMetadata()
        article_urls = response.css('div[class = "caption-text"] a::attr(href)')

        # get volume and issue: first number after "volume" and first number
        # after "issue" in the url
        # inspect_response(response, self)
        vol_issue_url = response.request.url
        # item['volume'] = re.search("volume/(\d+)", vol_issue_url).group(1)
        # item['issue'] = re.search("issue/(\d+)", vol_issue_url).group(1)

        for url in article_urls:
        # some of article_urls include links to "collections";
        # avoid these links because they do not directly lead to the article
            if bool(re.search("collection", url.get())):
                continue
            full_url = f'{HOME}{url.get()}'
            request = scrapy.Request(url = full_url, callback = self.parse_article)
            request.meta['item'] = item
            yield request

    def parse_article(self, response):
        item = response.meta['item']

#
#
#         ######################### BeutifulSoup #################################
#         soup = BeautifulSoup(response.text, "html.parser")
#         # create dict to make sure that pdf is pdf and xml is xml, not the other way
#         xml_pdf = {f"{i.text}":f"{HOME}{i['href']}"for i in soup.find_all("a", class_ = "piwik_download")}
#         edited_dict = {}
#         for key, value in xml_pdf.items():
#             edited_dict[re.sub(r"[\s]", "", key)] = re.sub(r"[\s]", "", value)
#         print(edited_dict["XML(EN)"])
#         article_xml = edited_dict["XML(EN)"]
#         ########################################################################
#
        item['title'] = response.xpath('normalize-space(//div[@class="article-title"]/h1)').get()
        return item
#         year  = response.xpath('normalize-space(//div[@class="credit-block credit-separator"])').get()
#         item['publication_year'] = re.search("\d{4}$", year).group(0)
#         item['article_type'] = response.xpath('normalize-space(//div[@class="article-title"]/h4)').get()
#         item['doi'] = response.xpath('//div[@class="authors"]/span[@class="span-citation"]/a/text()').get()
#         item['url'] = response.request.url
#         item['pdf_url_download'] = edited_dict['PDF(EN)']
#
#
#         def get_url(section_title, variable_name):
#             select_link = response.xpath(f'//div/h2[contains(text(), "{section_title}")]/following-sibling::*/a')
#             if select_link != []:
#                 item[variable_name] = select_link.xpath('./@href').get()
#             else:
#                 item[variable_name] = 'NA'
#
#         # get_url("Peer Review", 'peer_review_url')
#         # get_url("Data Accessibility", 'data_accessibility_links')
#
#
#    #      peer_review = response.xpath('//div/h2[contains(text(), "Peer Review")]/following-sibling::p/a')
#    #      if peer_review != []:
#    #          item['peer_review_url'] = peer_review.xpath('./@href')
#    #      else:
#    #          item['peer_review_url'] = 'NA'
#    #
#    #      response.xpath('//div/h2[contains(text(), "Data Accessibility")]/followi
#    # ...: ng-sibling::p/a/@href').get()
#
#         request = scrapy.Request(url = article_xml, callback = self.parse_xml)
#         request.meta['item'] = item
#         yield request
#
#     def parse_xml(self, response):
#
#         item = response.meta['item']
#
#         ######################### BeutifulSoup #################################
#         soup = BeautifulSoup(response.text, "xml")
#         # get abstract
#         abs = soup.find('abstract')
#         if abs != None:
#             abstr = abs.p.text
#             abstr = re.sub("\s\s+" , " ", abstract).strip()
#             abstract = "".join(abstr.splitlines())
#         item['abstract'] = abstract
#
#         # get keywords
#         kwd = soup.find_all('kwd')
#         keyword = [keyword.text for keyword in kwd]
#         keys = ', '.join(keyword)
#         if keys != '':
#             keywords = keys
#         else:
#             keywords = 'NA'
#         item['keywords'] = keywords
#
#         return item
#
#
# # # 'abstract', 'keywords', 'url', 'pdf_url_download',
# # # 'peer_rev_url', 'conflict_of_interests', 'acknowledgements',
# # # 'data_acessibility', 'data_links', 'funding_info', 'author_contributions',
# # # 'views', 'downloads', 'altmetrics_score', 'altmetrics_total_outputs']
