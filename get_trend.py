import sys
import pandas as pd
import csv
from transformers import pipeline
import datetime
from GoogleNews import GoogleNews
from newspaper import Article
import requests
from gnews import GNews
import os

progress = 0

# La fonction pour récupérer des informations supplémentaires depuis un article
def get_more_info(url):
    response = requests.get(url)
    article = Article(url)
    article.set_html(response.content)
    article.parse()

    meta = article.meta_description
    contenu = article.text

    return meta, contenu

# La fonction pour récupérer les tendances
def top_news(article_language, article_country, time_period, article_number):
    
    client = GNews(language=article_language, country=article_country, period=time_period, start_date=None, end_date=None, max_results=article_number)
    articles = client.get_top_news()
    total = len(articles)
    df = pd.DataFrame({
        "Titre": [article['title'].split(' - ')[0] for article in articles],
        "Source": [article['title'].split(' - ')[1] for article in articles],
        "url" : [article['url'] for article in articles],
        "Date": [article['published date']for article in articles],
        "Description": [article['description']for article in articles]
    })  

    for i, index, row in df.iterrows():
        link = row['url']
        meta, contenu = get_more_info(link)
        df.at[index, 'Meta description'] = meta
        df.at[index, 'Contenu'] = contenu

    progress = int(((i + 1) / total) * 50)
    update_progress(progress)
    return df

def update_progress(value):
    with open('progress_trend.txt', 'w') as f:
        f.write(str(value))

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
    global progress
    articles = df["Contenu"]
    articles_sum_bart = []
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    count = 0
    total = len(articles)

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
            progress = 50 + int((count / total) * 50)
            update_progress(progress)
            print(f"----------- article numéro {count} completed ({progress}%). All informations are stored -----------")

    X = pd.DataFrame({'Résumé Bart': articles_sum_bart})
    return X

if __name__ == "__main__":
    global progress
    # Récupérer les arguments de la ligne de commande
    language = sys.argv[1]
    country = sys.argv[2]
    period = sys.argv[3]
    results = int(sys.argv[4])

    # Appeler la fonction trend_news avec les arguments récupérés
    df = top_news(language, country, period, results)
    df.to_csv("choix_trend.csv", sep=";", index=False)

    # Lecture de chaque ligne du fichier CSV et traitement individuel
    with open('choix_trend.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = []
        for row in reader:
            data.append(row)

    info = pd.DataFrame(data)
    X = summarize_w_bart(info)
    final_df = pd.concat([info, X], axis=1)
    final_df.to_csv("article_tendance_sum.csv", sep=";", index=False, quoting=csv.QUOTE_ALL)

    # Création du fichier choix_utilisateur_trend.csv si non existant
    if not os.path.exists("choix_utilisateur_trend.csv"):
        final_df.to_csv("choix_utilisateur_trend.csv", sep=";", index=False, quoting=csv.QUOTE_ALL, mode='w')
    
    update_progress(100)
