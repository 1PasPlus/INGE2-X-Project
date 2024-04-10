from bs4 import BeautifulSoup
import requests
import csv
#nterwebsite you wish to pull from that has news articles
res = requests.get('http://money.cnn.com/')
soup = BeautifulSoup(res.text, 'lxml')
#need to pul the ulcode from the website by right clicking and choosing inspecting element
news_box = soup.find('ul', {'class': '_6322dd28 ad271c3f'})
#drill down into the li's as they should always show a, which signals the header for the news article shown.
all_news = news_box.find_all('a')

for news in all_news:
  test=  (news.text)
  print(test)
with open('index.csv', 'w') as fobj:
    csvwriter = csv.writer(fobj, delimiter=',')
    for row in test:
        csvwriter.writerow(test)