import csv
from transformers import pipeline
import pandas as pd 

def summarize_w_bart (text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    sum = summarizer(text, max_length=1000, min_length=30, do_sample=False)
    return sum

def summarize_w_falcon (text):
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    sum = summarizer(text, max_length=1000, min_length=30, do_sample=False)
    return sum

df = pd.read_csv('choix_tendances.csv',delimiter=";")
articles = df["Contenu"]
articles_sum_bart = []
articles_sum_falcon = []

for article in articles:
    
    #print(article)
    sum_bart = summarize_w_bart(article)
    summary_text_bart = sum_bart[0]['summary_text']
    articles_sum_bart.append(summary_text_bart)

    sum_falcon = summarize_w_falcon(article)
    summary_text_falcon = sum_falcon[0]['summary_text']
    articles_sum_falcon.append(summary_text_falcon)



#print(articles_sum)
X = pd.DataFrame({'Résumé Bart': articles_sum_bart,
                  'Résumé Falcon':articles_sum_falcon})

# Sauvegarder le DataFrame dans un fichier CSV
X.to_csv("article_sum.csv", sep=";", index=False, quoting=csv.QUOTE_ALL)


#Best summarization is Bart model 