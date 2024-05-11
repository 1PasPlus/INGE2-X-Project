import subprocess
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

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
def home():
    return render_template('index.html')

@app.route('/search_topic', methods=['GET', 'POST'])
def search_topic():
    if request.method == 'POST':
        keyword = request.form['keyword']
        language = request.form['language']
        period = request.form['period']
        country = request.form['country']
        
        # Exécuter le script Python get_topic.py avec les arguments spécifiés
        subprocess.run(['python', 'get_topic.py', keyword, language, country, period])
        
        return render_template('search_topic.html', supported_languages=supported_languages, supported_countries=supported_countries)

    return render_template('search_topic.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/search_trend', methods=['GET', 'POST'])
def search_trend():
    if request.method == 'POST':
        language = request.form['language']
        country = request.form['country']
        period = request.form['period']
        results = request.form['results']
        
        # Exécuter le script Python get_trend.py avec les arguments spécifiés
        subprocess.run(['python', 'get_trend.py', language, country, period, results])
        
        return render_template('search_trend.html', supported_languages=supported_languages, supported_countries=supported_countries)
    
    return render_template('search_trend.html', supported_languages=supported_languages, supported_countries=supported_countries)

@app.route('/show_results/<string:type>', methods=['GET', 'POST'])
def show_results(type):
    if request.method == 'POST':
        selected_article_id = request.form.get('selected_article')
        # Redirige vers une route qui montre les détails de l'article choisi
        return redirect(url_for('show_article', type=type, article_id=selected_article_id))

    file_name = 'article_tendance_sum.csv' if type == 'tendance' else 'article_topic_sum.csv'
    data = pd.read_csv(f'static/{file_name}')
    articles = data.to_dict(orient='records')
    return render_template('show_results.html', articles=articles, type=type)

@app.route('/show_article/<string:type>/<int:article_id>')
def show_article(type, article_id):
    file_name = 'article_tendance_sum.csv' if type == 'tendance' else 'article_topic_sum.csv'
    data = pd.read_csv(f'static/{file_name}')
    article = data[data['id'] == article_id].to_dict(orient='records')[0]
    return render_template('show_article.html', article=article)

if __name__ == '__main__':
    app.run(debug=True)

