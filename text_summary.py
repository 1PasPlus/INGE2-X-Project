#from transformers import pipeline
import pandas as pd 

df = df = pd.read_csv('choix_tendances.csv')

#summarizer = pipeline("summarization", model="Falconsai/text_summarization")

article = df["Contenu"]
print(article)

##print(summarizer(article, max_length=1000, min_length=30, do_sample=False))
#>>> [{'summary_text': 'Hugging Face has emerged as a prominent and innovative force in NLP . From its inception to its role in democratizing AI, the company has left an indelible mark on the industry . The name "Hugging Face" was chosen to reflect the company\'s mission of making AI models more accessible and friendly to humans .'}]
