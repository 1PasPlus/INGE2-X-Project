import requests
import pandas as pd

api_key = 'ca04114e68ca4f0fb81651c1c301027a'
parameters = {
    'q': 'actualités',
    'language': 'fr',
    'apiKey': api_key
}

url = 'https://newsapi.org/v2/top-headlines'
response = requests.get(url, params=parameters)
data = response.json()

if data['status'] == 'ok':
    if data['totalResults'] > 0:
        articles_info = []
        for article in data['articles']:
            title = article['title']
            author = article.get('author', 'N/A')
            date = article['publishedAt']
            content = article['description']
            articles_info.append({'Title': title, 'Author': author, 'Date': date, 'Content': content})
        df = pd.DataFrame(articles_info)
        print(df)
    else:
        print("Aucun résultat trouvé.")
else:
    print('Erreur lors de la récupération des actualités:', data['message'])

print(df)
