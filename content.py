import re
import sys
import pandas as pd
from openai import OpenAI
import csv
import os

def extract_summary_bart():

    df = pd.read_csv('choix_utilisateur.csv', delimiter=';')

    # Sélectionner la valeur de la colonne "Résumé Bart" pour la première ligne
    resume_bart_column = df.iloc[0]['Résumé Bart']

    # Remplacer les valeurs manquantes par une chaîne vide
    if pd.isna(resume_bart_column):
        resume_bart_column = ''

    # Renvoyer la valeur de resume_bart_column en tant que chaîne de caractères
    return resume_bart_column


#OPENAI_API_KEY = '<secret_key>'

client = OpenAI(api_key="OPEN_API_KEY")

def create_content(prompts):
    # Définir les messages d'entrée
    messages = [
        {
            "role": "system", "content": "You are a helpful assistant."}
    ]

    # Liste pour stocker les réponses générées
    responses = []

    # Boucle sur les prompts d'entrée
    for prompt in prompts:
        # Ajouter le prompt d'entrée aux messages
        messages.append(
            {
                "role": "user",
                "content": prompt
            },
        )

        # Générer une réponse à partir du modèle de langage
        chat = client.chat.completions.create(model="gpt-3.5-turbo",messages=messages)     # temperature=1 et n=1

        # Extraire la réponse générée
        reply = chat.choices[0].message.content

        # Ajouter la réponse générée aux messages
        messages.append(
            {
                "role": "assistant",
                "content": reply
            },
        )

        # Ajouter la réponse générée à la liste de réponses
        responses.append(reply)

    # Renvoie la liste de réponses générées
    #print("-----\n")
    tweet = responses[-1]
    #print(tweet)
    
    return tweet

def get_prompt(type,summary):
     
    with open('Prompt/debut.txt', 'r') as f:
        text = f.read()
    with open('Prompt/suite_1.txt', 'r') as g:
        text_1 = g.read()
    with open('Prompt/suite_2.txt', 'r') as h:
        text_2 = h.read()
    with open('Prompt/suite_1_emoji.txt', 'r') as j:
        text_1_emoji = j.read()
    with open('Prompt/suite_2_emoji.txt', 'r') as k:
        text_2_emoji = k.read()
    with open('Prompt/suite_1_long.txt', 'r') as j:
        text_1_long = j.read()
    with open('Prompt/suite_2_long.txt', 'r') as k:
        text_2_long = k.read()
    with open('Prompt/suite_1_thread.txt', 'r') as j:
        text_1_thread = j.read()
    with open('Prompt/suite_2_thread.txt', 'r') as k:
        text_2_thread = k.read()
    
    prompt_input = text_2 + "\n\n" + summary + "\n\n"
    prompt_input_emoji = text_2_emoji + "\n\n" + summary + "\n\n"
    prompt_input_long = text_2_long + "\n\n" + summary + "\n\n"
    prompt_input_thread = text_2_thread + "\n\n" + summary + "\n\n"
    
    prompts = [text, text_1, prompt_input]
    prompts_emoji = [text, text_1_emoji, prompt_input_emoji]
    prompts_long = [text, text_1_long, prompt_input_long]
    prompts_thread = [text, text_1_thread, prompt_input_thread]

    if type == "1":
        return prompts
    
    elif type == "2":
        return prompts_emoji

    elif type == "3":
        return prompts_long
    
    elif type == "4":
        return prompts_thread

if __name__ == "__main__":
    
    choix_user = sys.argv[1]
    summary = extract_summary_bart()
    

    prompt = get_prompt(choix_user,summary)

    #print(f'--------------------------{prompt}')
    
    tweet = create_content(get_prompt(choix_user,summary))

    #print(f'--------------------------{tweet}')
    #print(type(tweet))

    resultat = re.search(r'"(.*?)"', tweet)

    # Vérification si un résultat a été trouvé
    if resultat:
        texte_isole = resultat.group(1)
        print(texte_isole)  # Affiche le texte entre guillemets
    else:
        print("Aucun texte entre guillemets trouvé")

    # Vérification du type
    print(type(texte_isole))  # Affiche <class 'str'>

    df = pd.read_csv('choix_utilisateur.csv', sep=';')

    # Ajouter une colonne 'tweet' avec le contenu de texte_isole
    df['tweet'] = texte_isole

    # Enregistrer le fichier CSV mis à jour
    df.to_csv('choix_utilisateur.csv', sep=';', index=False) 

