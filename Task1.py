import pandas as pd
import datetime
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
import requests

# Fonction pour récupérer la description d'un article à partir de son URL
def get_article_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Trouver la balise contenant la description de l'article
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            return description['content']
        else:
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de la description de l'article : {e}")
        return None

gnews = GoogleNews()

gnews.set_time_range('01/03/2024','16/03/2024')

gnews.search('bitcoin')

results = gnews.results()


# Créez une liste pour stocker les informations des articles
articles_info = []

# Parcourez chaque élément de votre liste de résultats
for result in results:
    # Obtenez la description de l'article en utilisant la fonction définie ci-dessus
    description = get_article_description(result['link'])
    print(description)
    # Créez un dictionnaire pour stocker les informations de l'article
    article_info = {
        'Title': result['title'],
        'Media': result['media'],
        'Date': result['date'],
        'Link': result['link'],
        'Description': description
    }
    # Ajoutez ce dictionnaire à la liste articles_info
    articles_info.append(article_info)

# Utilisez la liste pour créer un DataFrame pandas
df = pd.DataFrame(articles_info)
print(df)
# Affichez le DataFrame
print(df.info())


