import pandas as pd
import csv
from transformers import pipeline
import datetime
from GoogleNews import GoogleNews
from newspaper import Article
import requests
from gnews import GNews

#La librairie GoogleNews ne nous donne pas assez d'infos à mon goût donc j'utilise une autre méthode pour gratter qlq infos de plus (voir fonction suivante)

def get_more_info(url):
    response = requests.get(url)
    article = Article(url)
    article.set_html(response.content)
    article.parse()

    meta = article.meta_description
    contenu = article.text

    return meta, contenu

def topic_news(keyword,language,period):

    getnews = GoogleNews()
    getnews.set_lang(language)
    getnews.set_encode('utf-8')
    getnews.set_period(period)

    #getnews = GoogleNews(language,period,encore="utf-8")

    getnews.search(keyword)
    results = getnews.results()

    articles_info = []

    for result in results:
        #Les url renvoyés par GoogleNews ne sont pas valables, avec un peu de recherche je me suis apperçu qui fallait les slipts avant le premier & dans l'url
        #Exemple 
        #Url renoyé par GoogleNews : https://cryptopotato.com/this-happened-on-coinbases-bitcoin-premium-index-before-btc-plunged-to-66k/&ved=2ahUKEwj_to_CyPuEAxWiVqQEHY8kD1kQxfQBegQIABAC&usg=AOvVaw1tRkOHCP-kHNJq5LaGn-7D/
        #Url valide : https://cryptopotato.com/this-happened-on-coinbases-bitcoin-premium-index-before-btc-plunged-to-66k/
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
        
        #Ca on s'en fout notre code marche 
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
        "Date": [article['published date']for article in articles],
        "Description": [article['description']for article in articles]
    })  

    for index, row in df.iterrows():
        link = row['url']
        meta, contenu = get_more_info(link)
        df.at[index, 'Meta description'] = meta
        df.at[index, 'Contenu'] = contenu

    return df

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

def summarize_w_bart (df):

    articles = df["Contenu"]
    articles_sum_bart = []
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    count = 0
    
    for article in articles:
        summaries = []  # Réinitialiser la liste des résumés pour chaque nouvel article
        
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
            if display_list == 1:
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
            if display_list == 1:
                print(supported_countries)
            else:
                pass
    
    range = str(input("\n\nSur combien de jour souhaiter vous couvrir l'info en tendance?\nEntrez un nombre entier : "))
    time_range = range + 'd'
    nb_results = int(input("\n\nCombien de résultats souhaitez-vous afficher? "))

    df = top_news(speak, nationality, time_range, nb_results)
    df.to_csv("choix_tendances.csv", sep=";", index=False)

    # Lecture de chaque ligne du fichier CSV et traitement individuel
    with open('choix_tendances.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = []
        for row in reader:
            data.append(row)

    info = pd.DataFrame(data)
    X = summarize_w_bart(info)
    final_df = pd.concat([info, X], axis=1)
    final_df.to_csv("article_tendance_sum.csv", sep=";", index=False, quoting=csv.QUOTE_ALL)
    
elif choix == "2":
    keyword = input("\n\nEntrez votre mot-clé : ")
    range = str(input("\n\nSur combien de jour souhaiter vous couvrir l'info sur votre sujet?\nEntrez un nombre entier : "))
    time_range = range + 'd'
    speak = input("Dans quelle langue voulez-vous l'info (fr, en, it, etc) : ")

    df = topic_news(keyword,speak,time_range)
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

else:
    print("Choix invalide.")
    exit()