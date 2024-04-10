import pandas as pd
from gnews import GNews

client = GNews(language="fr", country="FR", period='7d', start_date=None, end_date=None, max_results=10)
choix = input("Voulez-vous des actualités Top du moment (1) ou des actualités en rapport avec un mot-clé (2) ? ")

if choix == "1":
    articles = client.get_top_news()

elif choix == "2":
    keyword = input("Entrez votre mot-clé : ")
    articles = client.get_news(keyword)
else:
    print("Choix invalide.")
    exit()

df = pd.DataFrame({
    "Titre": [article['title'].split(' - ')[0] for article in articles],
    "Source": [article['title'].split(' - ')[1] for article in articles],
    #"source2" : [article['publisher'] for article in articles], mauvais format "{'href': 'https://www.20minutes.fr'
    "url" : [article['url'] for article in articles],
    "published date": [article['published date']for article in articles],
    "description": [article['description']for article in articles]
})

df.to_csv("news.csv", index=False)

#seconde parti recherche des token "tag"

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import csv
import re
from collections import Counter

# Télécharger les ressources nécessaires pour nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Fonction de prétraitement du texte
def preprocess_text(text):
    # Suppression des caractères spéciaux et de la ponctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Suppression des mots vides
    stop_words = set(stopwords.words('french'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

# Chargement des données et construction du corpus
corpus = []

with open('news.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title_tokens = preprocess_text(row['Titre'])
        description_tokens = preprocess_text(row['description'])
        corpus.append(title_tokens + description_tokens)

# Calcul des tags pour chaque ligne du corpus
tags_list = []

for article_tokens in corpus:
    tags = Counter(article_tokens).most_common(5)
    tags_list.append(tags)

# Ajout des tags dans le fichier CSV
with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['tags']
    rows = list(reader)

with open('news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, row in enumerate(rows):
        row['tags'] = ', '.join([tag[0] for tag in tags_list[i]])
        writer.writerow(row)

print("Tags ajoutés au fichier CSV avec succès!")

