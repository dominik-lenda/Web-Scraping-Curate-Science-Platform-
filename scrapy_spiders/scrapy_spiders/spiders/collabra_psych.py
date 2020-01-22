# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
import re
from scrapy_spiders.items import CollabraPsychMetadata


HOME = 'https://www.collabra.org'

class CollabraPsychSpider(scrapy.Spider):
    name = 'collabra_psych'

    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title', 'publication_year', 'article_type', 'issue',
    'volume', 'doi', 'abstract', 'keywords', 'url', 'pdf_url_download',
    'peer_rev_url', 'conflict_of_interests', 'acknowledgements',
    'data_acessibility', 'data_links', 'funding_info', 'author_contributions',
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

# remove collections; if articles or sth
    def parse_volume(self, response):
        article_urls = response.css('div[class = "caption-text"] a::attr(href)')
        # some of article_urls include links to "collections";
        # avoid these links because they do not directly lead to the article
        for url in article_urls:
            if bool(re.search("collection", url.get())):
                continue
            full_url = f'{HOME}{url.get()}'
            yield scrapy.Request(url = full_url, callback = self.parse_article)

    def parse_article(self, response):
        item = CollabraPsychMetadata()

        item['title'] = response.css('div[class="article-title"] h1::text').get()

        year  = response.xpath('normalize-space(//div[@class="credit-block credit-separator"])').get()
        item['publication_year'] = re.search("\d{4}$", year).group(0)

        return(item)




        # # get DOI
        # doi = soup.find('article-id').text
        # d['doi'].append(doi)
        #
        # # get info about the type of article
        # art_type = soup.find('subject').text
        # d['article_type'].append(art_type)
        #
        # # get abstract's content
        # abs = soup.find('abstract')
        # if abs != None:
        #     abstract = abs.p.text
        #     abstract = re.sub("\s\s+" , " ", abstract) # edit, remove more
        #                                                # than one space
        # else:
        #     abstract = "NA"
        # d['abstract'].append(abstract)
        #
        # # Keywords
        # kwd = soup.find_all('kwd')
        # keyword = [keyword.text for keyword in kwd]
        # keys = ', '.join(keyword)
        # if keys != '':
        #     keywords = keys
        # else:
        #     keywords = 'NA'
        # d['keywords'].append(keywords)
        #
        # conf_int = extract_text("sec", "conflict of interest|competing interests")
        # d["conflict_of_interests"].append(conf_int)
        #
        # # materials
        #
        # materials = extract_text("sec", "materials")
        # d['materials'].append(materials)
        #
        # # extract all urls from materials
        # materials_url = extract_url("sec", "materials", "ext-link")
        # d['materials_urls'].append(materials_url)
        #
        # # get html url
        # html = str(soup.find("self-uri"))
        # url_html = re.sub('"','',re.search(r'".*"', html).group(0))
        # d['article_html_url'].append(url_html)
        #
        # # get url to pdf to download
        # pdf_download = edited_dict["PDF(EN)"]
        # d['pdf_url_download'].append(pdf_download)
        #
        # # acknowledgements
        # ack = extract_text("ack", "acknowledgement")
        # d['acknowledgements'].append(ack)
        #
        # # data accessibility
        # data_access = extract_text("sec", "data accessibility")
        # d['data_acessibility'].append(data_access)
        #
        # # extract urls from data_accessibility section
        # data_access_url = extract_url("sec", "data accessibility", "ext-link")
        # # print(data_access_url)
        # d['data_links'].append(data_access_url)
        #
        # # different titles for funding info section
        # fund_info = extract_text("sec", "funding information|funding statement")
        # d['funding_info'].append(fund_info)
        #
        # # different titles for authors contribution section
        # author_contrib = extract_text("sec",
        # "authors contributions|author contribution|authors contribution")
        # d['author_contribution'].append(author_contrib)
        #
        # # additional files
        # add_files = extract_text("sec", "additional file")
        # d['additional_files'].append(add_files)
        #
        # add_files_links = extract_url("sec", "additional file", "ext-link")
        # d['additional_files_urls'].append(add_files_links)
        #
        #
        #
