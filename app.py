from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import csv
import os

# Définition des langues et des pays pris en charge
supported_countries = {
    'Australia': 'AU', 'Botswana': 'BW', 'Canada ': 'CA', 'Ethiopia': 'ET', 'Ghana': 'GH', 'India ': 'IN',
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

supported_languages = {
    'english': 'en', 'indonesian': 'id', 'czech': 'cs', 'german': 'de', 'spanish': 'es-419', 'french': 'fr',
    'italian': 'it', 'latvian': 'lv', 'lithuanian': 'lt', 'hungarian': 'hu', 'dutch': 'nl', 'norwegian': 'no',
    'polish': 'pl', 'portuguese brasil': 'pt-419', 'portuguese portugal': 'pt-150', 'romanian': 'ro', 'slovak': 'sk',
    'slovenian': 'sl', 'swedish': 'sv', 'vietnamese': 'vi', 'turkish': 'tr', 'greek': 'el', 'bulgarian': 'bg',
    'russian': 'ru', 'serbian': 'sr', 'ukrainian': 'uk', 'hebrew': 'he', 'arabic': 'ar', 'marathi': 'mr', 'hindi': 'hi',
    'bengali': 'bn', 'tamil': 'ta', 'telugu': 'te', 'malyalam': 'ml', 'thai': 'th', 'chinese simplified': 'zh-Hans',
    'chinese traditional': 'zh-Hant', 'japanese': 'ja', 'korean': 'ko'
}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_topic', methods=['GET', 'POST'])
def search_topic():
    if request.method == 'POST':
        keyword = request.form['keyword']
        language = request.form['language']
        period = request.form['period']
        country = request.form['country']
        
        # Appeler la fonction pour récupérer les actualités par topic
        os.system(f'python get_topic.py {keyword} {language} {period} {country}')
        
        # Rediriger vers la page de résultats
        return redirect(url_for('show_results', search_type='topic'))
    
    return render_template('search_topic.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/search_trend', methods=['GET', 'POST'])
def search_trend():
    if request.method == 'POST':
        language = request.form['language']
        country = request.form['country']
        period = request.form['period']
        results = request.form['results']
        
        # Appeler la fonction pour récupérer les tendances
        os.system(f'python get_trend.py {language} {country} {period} {results}')
        
        # Rediriger vers la page de résultats
        return redirect(url_for('show_results', search_type='trend'))
    
    return render_template('search_trend.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/show_results/<search_type>', methods=['GET', 'POST'])
def show_results(search_type):
    if search_type == 'topic':
        csv_file = 'article_topic_sum.csv'
        output_file = 'choix_utilisateur.csv'
    else:
        csv_file = 'article_tendance_sum.csv'
        output_file = 'choix_utilisateur.csv'
    
    if not os.path.exists(csv_file):
        return render_template('show_results.html', error_message="No results found.")
    
    df = pd.read_csv(csv_file, sep=';', quoting=csv.QUOTE_ALL)
    
    articles = df.to_dict(orient='records')
    
    if request.method == 'POST':
        selected_article_id = int(request.form['selected_article'])
        selected_article = articles[selected_article_id]
        
        # Sauvegarder le choix de l'utilisateur dans un nouveau fichier CSV
        selected_df = pd.DataFrame([selected_article])
        if os.path.exists(output_file):
            selected_df.to_csv(output_file, sep=';', index=False, quoting=csv.QUOTE_ALL)
        else:
            selected_df.to_csv(output_file, sep=';', index=False, quoting=csv.QUOTE_ALL)
        
        return render_template('show_article.html', article=selected_article)
    
    return render_template('show_results.html', articles=articles)

@app.route('/images/<filename>')
def get_image(filename):
    return redirect(url_for('static', filename=os.path.join('images', filename)))

import subprocess

@app.route('/create_content', methods=['GET', 'POST'])
def create_content():
    if request.method == 'POST':

        tweet_type = request.form['tweet_type']
        include_image = request.form['include_image']

        os.system(f'python content.py {tweet_type} {include_image}')

        csv_file = 'choix_utilisateur.csv'

        df = pd.read_csv(csv_file, sep=';', quoting=csv.QUOTE_ALL)
        article = df.to_dict(orient='records')[0]

        return render_template('summary.html', article=article)

    return render_template('create_content.html')
    
@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/end', methods=['POST'])
def end():
    # Exécutez le script post.py pour publier le tweet
    result = subprocess.run(["python3", "post.py"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return render_template('end.html')

if __name__ == '__main__':
    app.run(debug=True)
