#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import random
import re
import pandas as pd

# url = 'https://www.collabra.org/1/volume/1/issue/1/'
# page = requests.get(url)

infile = open("xml_4.xml","r")
contents = infile.read()

meta = []
soup = BeautifulSoup(contents,'xml')

# DOI
doi = soup.find('article-id').get_text()
print("doi", doi)
# Art type
art_type = soup.find('subject').get_text()
print("art_type", art_type)
# abstract
abstract = soup.find('abstract').get_text()
print("abstract", abstract)
# keywords
kwd = soup.find_all('kwd')
keywords = [keyword.get_text() for keyword in kwd]
print("keywords", keywords)
# conflict of interests


if soup.select_one('sec:contains("Conflict of Interest Declaration")') != None:
    conf_interest = soup.select_one('sec:contains("Conflict of Interest Declaration")')
elif soup.select_one('sec:contains("Competing Interests")') != None:
    conf_interest = soup.select_one('sec:contains("Competing Interests")')
else:
    conf_interest = "NA"

if conf_interest != "NA":
    conflict = conf_interest.find('p').get_text()
    print("conf of interest", conflict)
else:
    conflict = "NA"
    print("conf_in", conflict)
# peer review url
a = [p.get_text() for p in soup.find_all('sec') if bool(re.search("peer review", p.get_text(), re.IGNORECASE))]
if a != []:
    peer_rev_url = re.search("http:.*", a[0]).group(0)
else:
    peer_rev_url = "NA"

# if soup.select_one('sec:contains("peer review comments")') != None:
#     peer_review = soup.select_one('sec:contains("Peer review comments")')
#     peer_rev = peer_review.find('uri').get_text()
# else:
#     peer_rev = "NA"
#

print("peer rev", peer_rev_url)


# html url
s = str(soup.find("self-uri"))
url_html = re.sub('"','',re.search(r'".*"', s).group(0))
print("url_html", url_html)

# articl PDF ???

# Acknowledgment ???
if soup.find('ack') == None:
    acknow = "NA"
else:
    ack = soup.find('ack')
    ackn = ack.find_all('p')
    acknow = ', '.join(i.get_text() for i in ackn)

print(acknow)

# function to get unique values
def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


# all osf links
text_soup = soup.find_all(text = True)
text_soup_1 = [str(text) for text in text_soup]

r = re.compile(".*osf.*")
osf_list = list(filter(r.match, text_soup_1)) # Read Note
osf_url = unique(osf_list)
if osf_url == []:
    osf_url = "NA"

# Funding info
if soup.select_one('sec:contains("Funding Information")') != None:
    fund = soup.select_one('sec:contains("Funding Information")')
    fund_info = [f.get_text() for f in fund.find_all('p')]
else:
    fund_info = "NA"

print(fund_info)

# Author Contribution info
if soup.select_one('sec:contains("Author Contribution")') != None:
    author_c = soup.select_one('sec:contains("Author Contribution")')
    author_cont = [ac.get_text() for ac in author_c.find_all('p')]
else:
    author_cont =  "NA"

print(author_cont)

b = [p for p in soup.select('sec') if bool(re.search("data accessibility", p.get_text(), re.IGNORECASE))]
print(b.find('p'))
# print(b)



# osf? More links -> Acknowledgment, data statement, itd.
# text_soup_1 = (i.get_text() for i in text_soup)
#
# for i in text_soup:
#     print(i)
# print(text_soup_1)
# print(re.match("osf", text_soup))
#
# sentence data and link
# print(data_url)



# print(method.find('uri'))
