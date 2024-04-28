from flask import Flask, render_template, request
import subprocess

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
        
        # Exécuter le script Python get_topic.py avec les arguments spécifiés
        subprocess.run(['python', 'get_topic.py', keyword, language, period])
        
        return render_template('search_topic.html')

    return render_template('search_topic.html')

@app.route('/search_trend', methods=['GET', 'POST'])
def search_trend():
    if request.method == 'POST':
        language = request.form['language']
        country = request.form['country']
        period = request.form['period']
        results = request.form['results']
        
        # Exécuter le script Python get_trend.py avec les arguments spécifiés
        subprocess.run(['python', 'get_trend.py', language, country, period, results])
        
        return render_template('search_trend.html')

    return render_template('search_trend.html')

if __name__ == '__main__':
    app.run(debug=True)
