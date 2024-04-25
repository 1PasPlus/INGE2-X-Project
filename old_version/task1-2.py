import pandas as pd
import datetime
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
import requests
from newspaper import Article
import nltk

url = 'https://news.bitcoin.com/unveiling-mr-100-the-mystery-bitcoin-wallet-linked-to-upbits-cold-storage/'
article = Article(url)
article.download()
article.parse()

meta = article.meta_description
contenu = article.text
url = article.url
date = article.publish_date
title = article.title
media = article.source_url

donnees = {
    'URL': [url],
    'Titre': [title],
    'Date de publication': [date],
    'Contenu': [contenu],
    'Méta-description': [meta],
    'Media': [media]
}

df = pd.DataFrame(donnees)

print(df)
