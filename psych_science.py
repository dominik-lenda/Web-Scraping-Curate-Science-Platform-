#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# scraps metadata from Journal of Cognition
#
# (C) 2019 Dominik Lenda, Wroclaw, Poland
# email: dlenda1729@gmail.com
# -----------------------------------------------------------

# 3. Psychological Science: all articles since badges started in 2014 that have an
# "Open Practices" statement, i.e., starting at Volume 25 Issue 5, May 2014
# (though only 1 article in that issue); 0 in next issue; 6 articles in Issue 7)
#
#   Metadata to extract (from PDF and HTML):
#         • DOI, article type (don't think this is available), abstract text,
# "Keywords", # of downloads (from an article's "metrics" subpage; example),
# "Declaration of Conflicting Interests", article HTML URL (only if open access),
# article PDF URL (sci-hub URL), "Open Practices" statement (extract all URLs and
# save in open.content.URLs field), "Funding", and "Authors Contributions".
#
# for all journals, you only need to extract article title and year into the Google doc,
# because our DOI LOOKUP crossref functionality already automatically retrieves article title,
# authors, year, journal name, and citations (Web of Science).
#
# as you can see, this is going to be pretty messy and challenging.  actually,
# just preparing this info has made question whether it's even worth doing
# (at this current point in time), relative to the costs of doing so (idea of
# doing this now is to seed our DB w/ more content to make our platform more
# compelling to prospective investors/funders in acquiring our next round of funding).
#
# please let me know how feasible you think it is and roughly how much time you
#  think this would take you. (i'm going to post this information as a Github
# issue, so that it's easier to track progress.).   and any other thoughts/comments you may have....

import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd

article_url = "https://journals.sagepub.com/doi/full/10.1177/0956797614523297"
page = requests.get(article_url)

soup = BeautifulSoup(page.text, "html.parser")

# print(soup.prettify())


# DOI
a = soup.find("script")
print(a.dataLayer.push)
