import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import random
import re
import pandas as pd
import json


df = pd.read_excel('psychological_science.xlsx')

dois = df['doi']



api_altmetric_home = "https://api.altmetric.com/v1/doi/"
altmetric_urls = [f'{api_altmetric_home}{re.sub("https://doi.org/", "", doi)}' for doi in dois]
# altmetric_urls = altmetric_urls[1:3]

alt_score = []
alt_outputs = []

for altmetric_url in altmetric_urls:
    t = random.randrange(2, 5)
    time.sleep(t)
    page = requests.get(altmetric_url)
    soup = BeautifulSoup(page.text, "html.parser")
    dictio = soup.get_text()
    # print(dictio)
    d = json.loads(dictio)

    altmetrics_score = d['score']
    alt_score.append(altmetrics_score)
    print(altmetrics_score)
    total_outputs = d['context']['all']['count']
    alt_outputs.append(total_outputs)
    print(total_outputs)

df['altmetrics_score'] = alt_score
df['altmetrics_total_outputs'] = alt_outputs
df.to_excel("psych_science_FINAL.xlsx", encoding = 'utf-8', index = False)
