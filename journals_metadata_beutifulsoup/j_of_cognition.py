#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Scraps metadata from Journal of Cognition
#
# (C) 2019 Dominik Lenda, Wroclaw, Poland
# email dlenda1729@gmail.com
# -----------------------------------------------------------


import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import random
import re
import pandas as pd

# Metadata variables to scrap --------------------------------

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
# the unique title (see extract_text() and extract_url() functions)

# -----------------------------------------------------------
def extract_text(main_tag, title_name):
    """ Scrap section's text.
    Args:
    main_tag: if XML tag is <sec> or <ack>, main_tag argument is "sec",
    title_name: title of the section, e.g "funding information".

    Returns:
    Content of the section prepared to save inside the table or NA if paper
    does not include specified section
    """
    titles = soup.find_all("title")
    titles_list = [title.text for title in titles]
    bool_list = [bool(re.match(title_name, title, re.IGNORECASE))
    for title in titles_list]

    bool_value = any(bool_list)

    if bool_value == True:
        index = bool_list.index(True)
        title = titles_list[index]

        # extract section with specified title
        extracted_soup = soup.select_one(f'{main_tag}:contains("{title}")')
        content = re.sub(title, "", extracted_soup.text)
        # remove multiple whitespaces
        editing_content = re.sub("\s\s+" , " ", content)
        # remove white space in the beginning/at the end of the string
        edited_content = editing_content.strip()
        return edited_content
    else:
        # fill NA if section is not included
        edited_content = "NA"
        return edited_content


def extract_url(main_tag, title_name, url_tags):
        """ Extract all URLs from the section identified by the tag and the title.
        Args:
        main_tags: XML type tag, e.g. if <sec> is the tag, the argument is "sec",
        title_name: title of the section, e.g "funding information".
        url_tags: tag that identifies the url
        Returns:
        All urls from the scraped section.
        """

        titles = soup.find_all("title")
        titles_list = [title.text for title in titles]
        bool_list = [bool(re.match(title_name, title, re.IGNORECASE))
        for title in titles_list]

        bool_value = any(bool_list)

        if bool_value == True:
            index = bool_list.index(True)
            title = titles_list[index]

            # extract section with specified title
            final_content = soup.select_one(f'{main_tag}:contains("{title}")')
        else:
            final_content = "NA"

        if final_content != "NA":
            content = final_content.select(url_tags)
            print(content)
            if content != []:
                list_links = [i.text for i in content]
# ONE EMAIL APPEARD, get rid of it in the future
                get_final_content = "\n".join(list_links)
                return get_final_content
            else:
                return "NA"
        else:
            return "NA"



# creating dict to save excel file
d = {'title': [], 'publication_year': [] , 'issue': [],  'volume': [],
'doi': [], 'article_type': [], 'abstract': [], 'keywords': [],
'conflict_of_interests': [], 'materials': [], 'materials_urls': [],
'article_html_url': [], 'pdf_url_download': [], 'acknowledgements': [],
'data_acessibility': [], 'data_links': [], 'funding_info': [],
'author_contribution': [], 'additional_files': [], 'additional_files_urls': []}


HOME = "https://www.journalofcognition.org"

# list of volumes to scrap
volume_urls = ["https://www.journalofcognition.org/1/volume/1/issue/1/",
"https://www.journalofcognition.org/3/volume/2/issue/1/"]


for volume in volume_urls:

    volume_page = requests.get(volume)

    soup = BeautifulSoup(volume_page.text, "html.parser")

    links_short = [i['href'] for i in soup.find_all("a", class_ = "fa fa-eye")]
    links = [f'{HOME}{i}' for i in links_short]

    for art in links:
        # extract the issue and volume number
        issue_num = re.search('(?<=issue/)\d', volume).group(0)
        d['issue'].append(issue_num)

        volume_num = re.search('(?<=volume/)\d', volume).group(0)
        d['volume'].append(volume_num)

        t = random.randrange(2, 5)
        time.sleep(t)
        article_page = requests.get(art)
        soup = BeautifulSoup(article_page.text, "html.parser")

        # create dict to make sure that pdf is pdf and xml is xml, not the other way
        xml_pdf = {f"{i.text}":f"{HOME}{i['href']}"
        for i in soup.find_all("a", class_ = "piwik_download")}

        edited_dict = {}
        for key, value in xml_pdf.items():
            edited_dict[re.sub(r"[\s]", "", key)] = re.sub(r"[\s]", "", value)

        print(edited_dict["XML(EN)"])
        article_xml = edited_dict["XML(EN)"]

        page = requests.get(article_xml)

        soup = BeautifulSoup(page.text, "xml")

# metadata variables -------------------------------------

        # get title of an article
        article_title = soup.find("article-title").text
        # remove more than one whitespace
        article_title = re.sub("\s\s+" , " ", article_title)
        d['title'].append(article_title)

        # get year of publication
        article_year = soup.find("year").text
        d['publication_year'].append(article_year)

        # get DOI
        doi = soup.find('article-id').text
        d['doi'].append(doi)

        # get info about the type of article
        art_type = soup.find('subject').text
        d['article_type'].append(art_type)

        # get abstract's content
        abs = soup.find('abstract')
        if abs != None:
            abstract = abs.p.text
            abstract = re.sub("\s\s+" , " ", abstract) # edit, remove more
                                                       # than one space
        else:
            abstract = "NA"
        d['abstract'].append(abstract)

        # Keywords
        kwd = soup.find_all('kwd')
        keyword = [keyword.text for keyword in kwd]
        keys = ', '.join(keyword)
        if keys != '':
            keywords = keys
        else:
            keywords = 'NA'
        d['keywords'].append(keywords)

        conf_int = extract_text("sec", "conflict of interest|competing interests")
        d["conflict_of_interests"].append(conf_int)

        # materials

        materials = extract_text("sec", "materials")
        d['materials'].append(materials)

        # extract all urls from materials
        materials_url = extract_url("sec", "materials", "ext-link")
        d['materials_urls'].append(materials_url)

        # get html url
        html = str(soup.find("self-uri"))
        url_html = re.sub('"','',re.search(r'".*"', html).group(0))
        d['article_html_url'].append(url_html)

        # get url to pdf to download
        pdf_download = edited_dict["PDF(EN)"]
        d['pdf_url_download'].append(pdf_download)

        # acknowledgements
        ack = extract_text("ack", "acknowledgement")
        d['acknowledgements'].append(ack)

        # data accessibility
        data_access = extract_text("sec", "data accessibility")
        d['data_acessibility'].append(data_access)

        # extract urls from data_accessibility section
        data_access_url = extract_url("sec", "data accessibility", "ext-link")
        # print(data_access_url)
        d['data_links'].append(data_access_url)

        # different titles for funding info section
        fund_info = extract_text("sec", "funding information|funding statement")
        d['funding_info'].append(fund_info)

        # different titles for authors contribution section
        author_contrib = extract_text("sec",
        "authors contributions|author contribution|authors contribution")
        d['author_contribution'].append(author_contrib)

        # additional files
        add_files = extract_text("sec", "additional file")
        d['additional_files'].append(add_files)

        add_files_links = extract_url("sec", "additional file", "ext-link")
        d['additional_files_urls'].append(add_files_links)


df = pd.DataFrame(data=d)
df.to_excel("j_of_cognition_FINAL.xlsx", encoding = 'utf-8', index = False)
