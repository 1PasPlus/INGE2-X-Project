import pandas as pd
import datetime
from GoogleNews import GoogleNews
from newspaper import Article
import requests
from gnews import GNews
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import csv
import re
from collections import Counter

def get_more_info(url):
    response = requests.get(url)
    article = Article(url)
    article.set_html(response.content)
    article.parse()

    meta = article.meta_description
    contenu = article.text

    return meta, contenu

def topic_news(keyword,start,end):
    getnews = GoogleNews()
    getnews.set_time_range(start,end)
    getnews.search(keyword)
    results = getnews.results()

    articles_info = []
    for result in results:
        url = result['link'].split('&')[0]
        art = Article(url)
        try:
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
        except Exception as e:
            print("Erreur lors de la récupération des informations de l'article:", e)

    df = pd.DataFrame(articles_info)

    return df

def top_news(article_language, article_country, time_period, article_number):
    client = GNews(language=article_language, country=article_country, period=time_period, start_date=None, end_date=None, max_results=article_number)
    articles = client.get_top_news()

    df = pd.DataFrame({
        "Titre": [article['title'].split(' - ')[0] for article in articles],
        "Source": [article['title'].split(' - ')[1] for article in articles],
        "url" : [article['url'] for article in articles],
        "published date": [article['published date']for article in articles],
        "description": [article['description']for article in articles]
    })  

    for index, row in df.iterrows():
        link = row['url']
        meta, contenu = get_more_info(link)
        df.at[index, 'Meta description'] = meta
        df.at[index, 'Contenu'] = contenu

    return df

choix = input("Voulez-vous des actualités Top du moment (1) ou des actualités en rapport avec un mot-clé (2) ? ")

if choix == "1":
    supported_countries = {'Australia': 'AU', 'Botswana': 'BW', 'Canada ': 'CA', 'Ethiopia': 'ET', 'Ghana': 'GH', 'India ': 'IN',
            'Indonesia': 'ID', 'Ireland': 'IE', 'Israel ': 'IL', 'Kenya': 'KE', 'Latvia': 'LV', 'Malaysia': 'MY', 'Namibia': 'NA',
            'New Zealand': 'NZ', 'Nigeria': 'NG', 'Pakistan': 'PK', 'Philippines': 'PH', 'Singapore': 'SG', 'South Africa': 'ZA',
            'Tanzania': 'TZ', 'Uganda': 'UG', 'United Kingdom': 'GB', 'United States': 'US', 'Zimbabwe': 'ZW',
            'Czech Republic': 'CZ', 'Germany': 'DE', 'Austria': 'AT', 'Switzerland': 'CH', 'Argentina': 'AR', 'Chile': 'CL',
            'Colombia': 'CO', 'Cuba': 'CU', 'Mexico': 'MX', 'Peru': 'PE', 'Venezuela': 'VE', 'Belgium ': 'BE', 'France': 'FR',
            'Morocco': 'MA', 'Senegal': 'SN', 'Italy': 'IT', 'Lithuania': 'LT', 'Hungary': 'HU', 'Netherlands': 'NL',
            'Norway': 'NO', 'Poland': 'PL', 'Brazil': 'BR', 'Portugal': 'PT', 'Romania': 'RO', 'Slovakia': 'SK', 'Slovenia': 'SI',
            'Sweden': 'SE', 'Vietnam': 'VN', 'Turkey': 'TR', 'Greece': 'GR', 'Bulgaria': 'BG', 'Russia': 'RU', 'Ukraine ': 'UA',
            'Serbia': 'RS', 'United Arab Emirates': 'AE', 'Saudi Arabia': 'SA', 'Lebanon': 'LB', 'Egypt': 'EG',
            'Bangladesh': 'BD', 'Thailand': 'TH', 'China': 'CN', 'Taiwan': 'TW', 'Hong Kong': 'HK', 'Japan': 'JP',
            'Republic of Korea': 'KR'
            }
    supported_languages = {'english': 'en', 'indonesian': 'id', 'czech': 'cs', 'german': 'de', 'spanish': 'es-419', 'french': 'fr',
            'italian': 'it', 'latvian': 'lv', 'lithuanian': 'lt', 'hungarian': 'hu', 'dutch': 'nl', 'norwegian': 'no',
            'polish': 'pl', 'portuguese brasil': 'pt-419', 'portuguese portugal': 'pt-150', 'romanian': 'ro', 'slovak': 'sk',
            'slovenian': 'sl', 'swedish': 'sv', 'vietnamese': 'vi', 'turkish': 'tr', 'greek': 'el', 'bulgarian': 'bg',
            'russian': 'ru', 'serbian': 'sr', 'ukrainian': 'uk', 'hebrew': 'he', 'arabic': 'ar', 'marathi': 'mr', 'hindi': 'hi',
            'bengali': 'bn', 'tamil': 'ta', 'telugu': 'te', 'malyalam': 'ml', 'thai': 'th', 'chinese simplified': 'zh-Hans',
            'chinese traditional': 'zh-Hant', 'japanese': 'ja', 'korean': 'ko'
            }
    while True:
        speak = input("Dans quelle langue voulez-vous l'info (fr, en, it, etc) : ")
        if speak.lower() in supported_languages.values():
            break
        else:
            print("Langue non prise en charge. Veuillez réessayer.")
            display_list = input("Voulez-vous afficher la liste des langues disponibles?\nOui (1) Non(2) : ")
            if display_list == '1':
                print(supported_languages)
            else:
                pass

    while True:
        nationality = input("De quel pays souhaitez-vous que l'info vienne (FR, JP, US, etc) :  ")
        if nationality.upper() in supported_countries.values():
            break
        else:
            print("Pays non pris en charge. Veuillez réessayer.")
            display_list = input("Voulez-vous afficher la liste des pays dans lequel il est possible d'obtenir des news?\nOui (1) Non(2) : ")
            if display_list == '1':
                print(supported_countries)
            else:
                pass
    
    range = str(input("\n\nSur combien de jour souhaiter vous couvrir l'info en tendance?\nEntrez un nombre entier : "))
    time_range = range + 'd'
    nb_results = int(input("\n\nCombien de résultats souhaitez-vous afficher? "))

    df = top_news(speak, nationality, time_range, nb_results)
    df.to_csv("choix_tendances.csv", sep=";", index=False)

elif choix == "2":
    keyword = input("\n\nEntrez votre mot-clé : ")
    start = input("\n\nEntrez au format JJ/MM/AAAA la timeframe que vous souhaitez appliquer à votre recherche\nATTENTION ! Tous les résultats seront issus d'articles parus dans cet intervale de temps\nDate de début : ")
    end = input("\n\nDate de fin (au format JJ/MM/AAAA) : ")
    df = topic_news(keyword,start,end)
    print(df)
    print(df.info())

else:
    print("Choix invalide.")
    exit()


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

corpus = []

for index, row in df.iterrows():
    title_tokens = preprocess_text(row['Titre'])
    description_tokens = preprocess_text(row['description'])
    corpus.append(title_tokens + description_tokens)

tags_list = []

for article_tokens in corpus:
    tags = Counter(article_tokens).most_common(5)
    tags_list.append(tags)

df = pd.read_csv('choix_tendances.csv', delimiter=';')

for i, tags in enumerate(tags_list):
    df.at[i, 'Tags'] = ', '.join(tag[0] for tag in tags)

df.to_csv("choix_tendances_tags.csv", sep=";", index=False)

print("Tags ajoutés au fichier CSV avec succès!")
