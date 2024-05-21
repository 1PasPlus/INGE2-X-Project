import pandas as pd
import sys 
from transformers import pipeline
from GoogleNews import GoogleNews
from newspaper import Article
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import csv
import re
from collections import Counter

# Initialisation de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('french'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def generate_tags(df):
    corpus = []
    for index, row in df.iterrows():
        title_tokens = preprocess_text(row['Titre'])
        description_tokens = preprocess_text(row['Description'])
        corpus.append(title_tokens + description_tokens)

    tags_list = []
    for article_tokens in corpus:
        tags = Counter(article_tokens).most_common(5)
        tags_list.append(tags)

    for i, tags in enumerate(tags_list):
        df.at[i, 'Tags'] = ', '.join(tag[0] for tag in tags)

    return df

# Fonction pour interroger l'API pour générer une image à partir du texte
def generate_image_from_text(text):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content
    return image_bytes

def get_more_info(url):
    response = requests.get(url)
    article = Article(url)
    article.set_html(response.content)
    article.parse()

    meta = article.meta_description
    contenu = article.text

    return meta, contenu

# La fonction pour récupérer les actualités sur un sujet spécifique
def topic_news(keyword, language, location, time_range):

    getnews = GoogleNews(lang=language, region=location, period=time_range)

    getnews.search(keyword)
    results = getnews.results()

    articles_info = []

    for result in results:
        url = result['link'].split('&')[0]
        art = Article(url)

        try:
            meta, contenu = get_more_info(url)
            article_info = {
                'Titre': result['title'],
                'Source': result['media'],
                'url':  art.url,
                'Date': result['datetime'],
                'Description': result['desc'],
                'Meta description': meta,
                'Contenu': contenu
            }

            articles_info.append(article_info)
        
        except Exception as e:
            print("Erreur lors de la récupération des informations de l'article:", e)

    df = pd.DataFrame(articles_info)
    dfinal = generate_tags(df)
    # Initialiser une liste pour stocker les chemins des images
    image_paths = []

    # Itérer à travers chaque ligne du fichier CSV
    for index, row in dfinal.iterrows():
        # Récupérer le texte de l'article
        text = row['Description']
        # Générer l'image à partir du texte
        image_bytes = generate_image_from_text(text)
    
        # Enregistrer l'image avec un nom unique (par exemple, l'index de la ligne)
        image_path = f"static/images/image_topic_{index}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
    
        # Ajouter le chemin de l'image à la liste
        image_paths.append(image_path)

    # Ajouter la colonne "Image" au DataFrame
    dfinal['Image'] = image_paths
    return dfinal
    return dfinal

# Fonction pour résumer le contenu des articles
def split_into_segments(text, max_segment_length=1000):
    segments = []
    current_segment = ""
    words = text.split()
    for word in words:
        if len(current_segment) + len(word) < max_segment_length:
            current_segment += word + " "
        else:
            segments.append(current_segment.strip())
            current_segment = word + " "
    segments.append(current_segment.strip())
    return segments

def summarize_w_bart(df):

    articles = df["Contenu"]
    articles_sum_bart = []
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    count = 0
    
    for article in articles:
        summaries = []  
        
        if type(article) != str:
            pass
        
        else:
            segments = split_into_segments(article)
            
            for segment in segments:
                summary = summarizer(segment, max_length=1000, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            
    
            articles_sum_bart.append(" ".join(summaries))
            count += 1
            print("----------- article numéro", count,"completed. All informations are stored -----------")
    

    X = pd.DataFrame({'Résumé Bart': articles_sum_bart})

    return X

if __name__ == "__main__":
    # Récupérer les arguments de la ligne de commande
    keyword = sys.argv[1]
    language = sys.argv[2]
    period = sys.argv[3]
    region = sys.argv[4]

    # Appeler la fonction topic_news avec les arguments récupérés
    df = topic_news(keyword, language, region, period)
    df.to_csv("choix_topic.csv", sep=";", index=False)

    # Lecture de chaque ligne du fichier CSV et traitement individuel
    with open('choix_topic.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = []
        for row in reader:
            data.append(row)

    info = pd.DataFrame(data)
    X = summarize_w_bart(info)
    final_df = pd.concat([info, X], axis=1)
    final_df.to_csv("article_topic_sum.csv", sep=";", index=False, quoting=csv.QUOTE_ALL)