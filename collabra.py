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

infile = open("xml_2.xml","r")
contents = infile.read()

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

def get_info(phrase):
    info = [sec.p.text for sec in soup.find_all('sec') if bool(re.search(phrase, str(sec.title), re.IGNORECASE))]
    if info != []:
        return info
    else:
        return "NA"

a = get_info("interest")
print(a)

b = get_info("peer review")
print(b)

# html url
s = str(soup.find("self-uri"))
url_html = re.sub('"','',re.search(r'".*"', s).group(0))
print("url_html", url_html)

# Acknowledgment ???
if soup.find('ack') != None:
    ack = soup.find('ack').p
    print(ack.text)
else:
    acknow = "NA"

data_access = get_info("data accessibility")
print(data_access)

fund_info = get_info("funding info")
print(fund_info)

author_contrib = get_info("author contribution")
print(author_contrib)
