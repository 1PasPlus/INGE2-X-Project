import pandas as pd
from gnews import GNews


client = GNews(language="fr", country="FR", period='7d', start_date=None, end_date=None, max_results=3)
choix = input("Voulez-vous des actualités Top du moment (1) ou des actualités en rapport avec un mot-clé (2) ? ")

if choix == "1":
    articles = client.get_top_news()

elif choix == "2":
    keyword = input("Entrez votre mot-clé : ")
    articles = client.get_news(keyword)
else:
    print("Choix invalide.")
    exit()

if articles:
    df = pd.DataFrame({
        "Titre": [article['title'].split(' - ')[0] for article in articles],
        "Source": [article['title'].split(' - ')[1] for article in articles],
        #"source2" : [article['publisher'] for article in articles], mauvais format "{'href': 'https://www.20minutes.fr'
        "url" : [article['url'] for article in articles],
        "published date": [article['published date']for article in articles],
        "description": [article['description']for article in articles]

    })

    df.to_csv("news.csv", index=False)
else:
    print("Aucune actualité trouvée")
