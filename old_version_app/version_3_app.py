from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import os
import time
import csv 

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

progress = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_topic', methods=['GET', 'POST'])
def search_topic():
    global progress
    if request.method == 'POST':
        keyword = request.form['keyword']
        language = request.form['language']
        period = request.form['period']
        country = request.form['country']
        
        # Reset progress
        progress = 0
        
        # Appeler la fonction pour récupérer les actualités par topic
        os.system(f'python get_topic.py {keyword} {language} {period} {country} &')
        
        # Rediriger vers la page de résultats avec une barre de chargement
        return redirect(url_for('loading', search_type='topic'))
    
    return render_template('search_topic.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/search_trend', methods=['GET', 'POST'])
def search_trend():
    global progress
    if request.method == 'POST':
        language = request.form['language']
        country = request.form['country']
        period = request.form['period']
        results = request.form['results']
        
        # Reset progress
        progress = 0
        
        # Appeler la fonction pour récupérer les tendances
        os.system(f'python get_trend.py {language} {country} {period} {results} &')
        
        # Rediriger vers la page de résultats avec une barre de chargement
        return redirect(url_for('loading', search_type='trend'))
    
    return render_template('search_trend.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/loading/<search_type>')
def loading(search_type):
    return render_template('loading.html', search_type=search_type)

@app.route('/progress')
def progress_status():
    global progress
    return jsonify({'progress': progress})

@app.route('/show_results/<search_type>', methods=['GET', 'POST'])
def show_results(search_type):
    if search_type == 'topic':
        csv_file = 'article_topic_sum.csv'
        output_file = 'choix_utilisateur_topic.csv'
    else:
        csv_file = 'article_tendance_sum.csv'
        output_file = 'choix_utilisateur_trend.csv'
    
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
            selected_df.to_csv(output_file, mode='a', header=False, sep=';', index=False, quoting=csv.QUOTE_ALL)
        else:
            selected_df.to_csv(output_file, sep=';', index=False, quoting=csv.QUOTE_ALL)
        
        return render_template('show_article.html', article=selected_article)
    
    return render_template('show_results.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)