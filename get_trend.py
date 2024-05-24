from gnews import GNews
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


def improve_prompt(text):
    LL_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
    payload = {"inputs": f"Generate a detailed image prompt for the following description: {text}"}
    response = requests.post(LL_API_URL, headers=headers, json=payload)
    response_json = response.json()
    
    # Vérifiez la structure de la réponse JSON
    if isinstance(response_json, list) and len(response_json) > 0:
        improved_text = response_json[0].get('generated_text', text).strip()  # Accédez au premier élément de la liste
    else:
        improved_text = text  # Si la réponse n'est pas conforme, utilisez le texte original

    return improved_text

# Fonction pour interroger l'API pour générer une image à partir du texte
def generate_image_from_text(text):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
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

def top_news(article_language, article_country, time_period, article_number):
    
    client = GNews(language=article_language, country=article_country, period=time_period, start_date=None, end_date=None, max_results=article_number)
    articles = client.get_top_news()

    df = pd.DataFrame({
        "Titre": [article['title'].split(' - ')[0] for article in articles],
        "Source": [article['title'].split(' - ')[1] for article in articles],
        "url" : [article['url'] for article in articles],
        "Date": [article['published date']for article in articles],
        "Description": [article['description']for article in articles]
    })  

    for index, row in df.iterrows():
        link = row['url']
        meta, contenu = get_more_info(link)
        df.at[index, 'Meta description'] = meta
        df.at[index, 'Contenu'] = contenu

    dfinal = generate_tags(df)
    
    # Initialiser une liste pour stocker les chemins des images
    image_paths = []

    # Itérer à travers chaque ligne du fichier CSV
    for index, row in dfinal.iterrows():
        # Récupérer le texte de l'article
        prompt = row['Description']
        # Améliorer le prompt qui génèrera l'image wsh
        improved_prompt = improve_prompt(prompt)
        # Générer l'image
        image_bytes = generate_image_from_text(improved_prompt)
    
        # Enregistrer l'image avec un nom unique (par exemple, l'index de la ligne)
        image_path = f"static/images/image_trend_{index}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
    
        # Ajouter le chemin de l'image à la liste
        image_paths.append(image_path)

    # Ajouter la colonne "Image" au DataFrame
    dfinal['Image'] = image_paths
    return dfinal

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
    article_language = sys.argv[1]
    article_country = sys.argv[2]
    article_period = sys.argv[3]
    article_number = sys.argv[4]

    #On reformate correctement les données
    language = article_language.lower()
    country = article_country.upper()
    time_range = article_period + 'd'
    n = int(article_number)
 
    df = top_news(language, country, time_range, n)
    df.to_csv("articles_tendances.csv", sep=";", index=False)

    with open('articles_tendances.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = []
        for row in reader:
            data.append(row)

    info = pd.DataFrame(data)
    X = summarize_w_bart(info)
    final_df = pd.concat([info, X], axis=1)
    final_df.to_csv("article_tendance_sum.csv", sep=";", index=False, quoting=csv.QUOTE_ALL)