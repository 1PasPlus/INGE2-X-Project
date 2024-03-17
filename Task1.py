import pandas as pd
import datetime
from GoogleNews import GoogleNews
from newspaper import Article
import requests

gnews = GoogleNews()
gnews.set_time_range('01/03/2024','16/03/2024')
gnews.search('bitcoin')
results = gnews.results()

#La librairie GoogleNews ne nous donne pas assez d'infos à mon goût donc j'utilise une autre méthode pour gratter qlq infos de plus (voir fonction suivante)

#On prendra ici des infos en plus qui se retrouveront plus tard dans notre dataframe 
def get_more_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    article = Article(url)
    article.set_html(response.content)
    article.parse()

    meta = article.meta_description
    contenu = article.text

    return meta, contenu


articles_info = []

#On fait une boucle pour tous les résultats trouvés par GoogleNews
for result in results:
    #Les url renvoyés par GoogleNews ne sont pas valables, avec un peu de recherche je me suis apperçu qui fallait les slipts avant le premier & dans l'url
    #Exemple 
    #Url renoyé par GoogleNews : https://cryptopotato.com/this-happened-on-coinbases-bitcoin-premium-index-before-btc-plunged-to-66k/&ved=2ahUKEwj_to_CyPuEAxWiVqQEHY8kD1kQxfQBegQIABAC&usg=AOvVaw1tRkOHCP-kHNJq5LaGn-7D/
    #Url valide : https://cryptopotato.com/this-happened-on-coinbases-bitcoin-premium-index-before-btc-plunged-to-66k/
    url = result['link'].split('&')[0]
    art = Article(url)
    #print(url)
    try:
        #On ajoute tts les infos dans un dico pour le dataframe final
        meta, contenu = get_more_info(url)
        article_info = {
            'Title': result['title'],
            'Media': result['media'],
            'Date': result['date'],
            'Link':  art.url,
            'Résumé': contenu,  
            'Meta description': meta
        }
        articles_info.append(article_info)
    #Ca on s'en fout notre code marche 
    except Exception as e:
        print("Erreur lors de la récupération des informations de l'article:", e)

#Petit dataframe des familles tu connais 
df = pd.DataFrame(articles_info)
#print(df.info())
print(df)

print(df['Link'])

