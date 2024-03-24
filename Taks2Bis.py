import pandas as pd
import datetime
from GoogleNews import GoogleNews
from newspaper import Article
import requests
from gnews import GNews

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
    #print(contenu)

    return meta, contenu

#Fonction qui nous donne les tops articles sur le sujet choisit par l'utilisateur
def topic_news(keyword):
    keyword = input("\n\nEntrez votre mot-clé : ")
    start = input("\n\nEntrez au format JJ/MM/AAAA la timeframe que vous souhaitez appliquer à votre recherche\nATTENTION ! Tous les résultats seront issus d'articles parus dans cet intervale de temps\nDate de début : ")
    end = input("\n\nDate de fin (au format JJ/MM/AAAA) : ")
    
    getnews = GoogleNews()
    getnews.set_time_range(start,end)
    getnews.search(keyword)
    results = getnews.results()

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
    #print(df)
    #print(df['Link'])
    #print(df.info())
    #print(df['Résumé'])
    #df.to_csv("choix_sujet.csv", sep=";", index=False)

    return df

#Fonction qui donne les tops articles en tendance, peu importe le sujet
def top_news(article_language, article_country, time_period, article_number):
    #time_range = str(input("Sur combien de jour souhaiter vous couvrir l'info en tendance?\nEntrez un nombre entier : "))
    #speek = str(input("Dans quelle langue voulez-vous l'info (fr, eng, it,) : "))
    #nb_resultats = int(input("Combien de résultats souhaitez-vous afficher? "))
    #nationality = str(input("De quel pays souhaitez-vous que l'info vienne? Exemple : FR, ENG, USA"))
    #time_range_1 = input("Entrez au format JJ/MM/AAAA la timeframe que vous souhaitez appliquer à votre recherche\nATTENTION ! Tous les résultats seront issus d'articles parus dans cet intervale de temps\nDate de début")
    #time_range_2 = input("Date de fin (au format JJ/MM/AAAA)")
    #client = GNews(language=speek, country=nationality, period=time_range+'d', start_date=None, end_date=None, max_results=nb_resultats)
    
    client = GNews(language=article_language, country=article_country, period=time_period, start_date=None, end_date=None, max_results=article_number)
    articles = client.get_top_news()

    df = pd.DataFrame({
        "Titre": [article['title'].split(' - ')[0] for article in articles],
        "Source": [article['title'].split(' - ')[1] for article in articles],
        #"source2" : [article['publisher'] for article in articles], mauvais format "{'href': 'https://www.20minutes.fr'
        "url" : [article['url'] for article in articles],
        "published date": [article['published date']for article in articles],
        "description": [article['description']for article in articles]
    })  

    # Récupération des liens de chaque ligne du DataFrame
    for index, row in df.iterrows():
        link = row['url']
        meta, contenu = get_more_info(link)
        df = df.append({
            'Meta description': meta,
            'Contenu': contenu 
            }, ignore_index=True
        )
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

    # Appel de la fonction top_news avec les paramètres validés
    df = top_news(speak, nationality, time_range, nb_results)
    print(df.info())
    print(df)
    df.to_csv("choix_tendances.csv", sep=";", index=False)

elif choix == "2":
    # Code pour le deuxième choix
    pass

else:
    print("Choix invalide.")
    exit()