#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Scraps metadata of articles from Journal of Cognition - uses HTML and XML
#
# (C) 2019 Dominik Lenda, Wroclaw, Poland
# email dlenda1729@gmail.com
# -----------------------------------------------------------

# Metadata variables of articles to scrap --------------------

# Type of a variable : XML tag
#
# doi : <article-id>
# abstract : <abstract>
# keywords : <kwd>
# acknowledgements : <ack>
#
# Other metadata variables do not have unique tag, the main tag is <sec>

# other metadata variables:
# conflict of interests, peer review url, article's url (html and pdf),
# data_accessibility, funding information, authors contribution : <sec>

# since no unique tag for these variables, the program scraps by
# the unique title (see get_text_long(), get_text_short() and get_url() functions)

import scrapy
from scrapy.shell import inspect_response
import re
from scrapy_spiders.items import JofCognitionMetadata
import json


HOME = 'https://www.journalofcognition.org'


class Journal_of_Cognition(scrapy.Spider):
    name = 'jofcognition'

    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title', 'publication_year', 'article_type', 'volume',
    'issue', 'doi', 'abstract', 'keywords', 'url', 'pdf_url_download',
    'peer_review_url', 'conflict_of_interests', 'acknowledgements', 'materials',
    'materials_urls', 'data_accessibility_statement', 'data_accessibility_links',
    'funding_info', 'author_contributions', 'views', 'downloads'],
    #, 'altmetrics_score', 'altmetrics_total_outputs'],
    }

    def start_requests(self):
        start_urls = ['https://www.journalofcognition.org/issue/archive/']
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
            item = JofCognitionMetadata()
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


    def parse_article_xml(self, response):

        def get_text_short(xpath):
            """ Simple function to get edited text or output 'NA'
            if the information is not avaialable'
            Args: xpath: XPath notation
            """
            text = response.xpath(f'normalize-space({xpath})').get()
            return "NA" if not text else text


        def get_url(tag, title):
            """ Extracts URLs.
            Args:
            tag: XML tag, e.g. <sec> or <ack>, main tag argument is "sec",
            title: title of the section, e.g "funding information".

            Returns:
            Content of the section prepared to save inside the table or NA if paper
            does not include specified section.
            Note: this method uses XPath function - translate() to
            make titles case INSENSITIVE.
            """
            content = response.xpath(f'//{tag}[contains(translate(.,\
 "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]')

            if content.xpath('.//ext-link').get() != None:
                url_list = content.xpath('.//ext-link')
                for url in url_list:
                    all = [url.xpath('normalize-space()').get() for url in url_list]
                    return ', '.join(all)
            elif content.xpath('.//uri').get() != None:
                url_list = content.xpath('.//uri')
                for url in url_list:
                    all = [url.xpath('normalize-space()').get() for url in url_list]
                    return ', '.join(all)
            else:
                return 'NA'


        def get_text_long(tag, *titles):
            """ Extracts text.
            Args:
            tag: XML tag, e.g. <sec> or <ack>, main tag argument is "sec",
            *titles: titles of the section, e.g "data accessibility statement"
            Note: uses *args syntax, thus various forms of the same title
            might be examined, e.g. conflict of interests, competing interests.

            Returns:
            Content of the section prepared to save inside the table or NA if paper
            does not include specified section.

            Note: this method uses XPath function - translate() to
            make titles case INSENSITIVE.
            """
            bullet_list = []
            for title in titles:
                xpath = f'//title[contains(translate(. ,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]'
                section = response.xpath(f'{xpath}/parent::{tag}')
<<<<<<< HEAD

                # if section with specific title matches
                if section != []:
                    # if section contains bullet points
                    if section.xpath('./list') != []:
                        for txt in response.xpath(f'{xpath}/parent::{tag}/descendant::p'):
                            bullet_point = txt.xpath('normalize-space()').get()
                            bullet_list.append(bullet_point)
                        edited_text = '. '.join(bullet_list)
                    else:
                        str_title = response.xpath(f'normalize-space({xpath})').get()
                        text = section.xpath('normalize-space()').get()
                        edited_text  = re.sub(str_title, "", text).strip()
                    break
                else:
                    edited_text = "NA"
            return edited_text
=======
                # if section includes bullet points, for clarity output each line in newline
                if section.xpath('./list') != []:
                    for txt in response.xpath(f'{xpath}/parent::{tag}/descendant::p'):
                        bullet_point = txt.xpath('normalize-space()').get()
                        bullet_list.append(bullet_point)
                    edited_text = '\n'.join(bullet_list)
                # if section is not bullet-pointed output as normal text
                else:
                    str_title = response.xpath(f'normalize-space({xpath})').get()
                    text = section.xpath('normalize-space()').get()
                if text != '':
                    break
            edited_text  = re.sub(str_title, "", text).strip()
            return "NA" if not edited_text else edited_text
>>>>>>> 8c06832534b51eb9995b9782c72f8df60f2fcc72

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
        item['acknowledgements'] = get_text_long('ack', 'acknowledgements')
        item['conflict_of_interests'] = get_text_long('sec', 'conflict of', 'competing interests')
        item['funding_info'] = get_text_long('sec', 'funding')
        item['author_contributions'] = get_text_long('sec', 'authors contribution', 'author contribution')
        item['data_accessibility_links'] = get_url('sec', 'data accessibility')
        item['materials'] = get_text_long('sec', 'materials')
        item['materials_urls'] = get_url('sec', 'materials')


        yield scrapy.Request(url = item['url'], callback = self.parse_article_html, meta={'item': item})

    def parse_article_html(self, response):
        def get_stats(stats):
            """ Extracts number of views and number of downloads.
            Args:
            stats: label of statistics, e.g. 'Views' or 'Downloads'
            Note: it is CASESENSITIVE

            Returns:
            Number of views or downloads of an article.
            """
            content = response.xpath(f'//div[@class="article-stats"]/\
            a[contains(., "{stats}")]/div[@class="stat-number"]/text()').get()
            return "NA" if not content else content
        item = response.meta['item']

        item['views'] = get_stats('Views')
        item['downloads'] = get_stats('Downloads')

        return item


        # add altmetrics score
    #     api_altmetric_home = "https://api.altmetric.com/v1/doi/"
    #     altmetric_url = f'{api_altmetric_home}{item["doi"]}'
    #     yield scrapy.Request(url = altmetric_url, callback = self.parse_altmetrics, meta={'item': item})
    #
    # def parse_altmetrics(self, response):
    #     item = response.meta["item"]
    #     dictionary_txt = response.css('p::text').get()
    #     d = json.loads(dictionary_txt)
    #     item['altmetrics_score'] = d['score']
    #     item['altmetrics_total_outputs'] = d['context']['all']['count']
