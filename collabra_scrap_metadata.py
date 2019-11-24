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

infile = open("xml_3.xml","r")
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
if soup.select_one('sec:contains("Peer review comments")') != None:
    peer_review = soup.select_one('sec:contains("Peer review comments")')
    peer_rev = peer_review.find('uri').get_text()
else:
    peer_rev = "NA"

print("peer rev", peer_rev)

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


# if soup.select_one('sec:contains("Materials and Methods")') != None:
#     method  = soup.select_one('sec:contains("Materials and Methods")')
# elif soup.select_one('sec:contains("Materials and Method")') != None:
#     method  = soup.select_one('sec:contains("Materials and Method")')
# else:
#     method = "NA"

# print(method)
# data_url = method.find("ext-link").get_text()

text_soup = soup.find_all(text = True)
text_soup_1 = [str(text) for text in text_soup]
for i in text_soup_1:
    print(i)

# function to get unique values
def unique(list1):

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print x,


print(type(text_soup_1))
r = re.compile(".*osf.*")
osf_list = list(filter(r.match, text_soup_1)) # Read Note
print(newlist)
# text_soup_1 = (i.get_text() for i in text_soup)

# for i in text_soup:
#     print(i)
# print(text_soup_1)
# print(re.match("osf", text_soup))

# sentence data and link
# print(data_url)



# print(method.find('uri'))

print("sth")
