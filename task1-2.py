import requests
import pandas as pd

# Remplacez 'YOUR_API_KEY' par votre clé d'API Google News
api_key = 'YOUR_API_KEY'

# Paramètres de requête pour l'API Google News
parameters = {
    'q': 'actualités',  # Recherche d'actualités générales
    'language': 'fr',   # Langue française
    'apiKey': api_key
}

# URL de l'API Google News
url = 'https://newsapi.org/v2/top-headlines'

# Envoi de la requête GET à l'API
response = requests.get(url, params=parameters)

# Conversion de la réponse en format JSON
data = response.json()

# Vérification si la requête a réussi
if data['status'] == 'ok':
    # Créer une liste pour stocker les informations des articles
    articles_info = []
    
    # Parcourir chaque article dans la réponse
    for article in data['articles']:
        # Extraire les informations pertinentes
        title = article['title']
        author = article.get('author', 'N/A')
        date = article['publishedAt']
        content = article['description']
        
        # Ajouter les informations à la liste
        articles_info.append({'Title': title, 'Author': author, 'Date': date, 'Content': content})
    
    # Créer un DataFrame à partir de la liste de dictionnaires
    df = pd.DataFrame(articles_info)
    
    # Afficher le DataFrame
    print(df)

else:
    print('Erreur lors de la récupération des actualités:', data['message'])
