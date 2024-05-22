import pandas as pd
import os

def extract_summary_bart():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    csv_path = os.path.join(parent_dir, 'article_tendance_sum.csv')

    df = pd.read_csv(csv_path, delimiter=';')

    # Sélectionner la valeur de la colonne "Résumé Bart" pour la première ligne
    resume_bart_column = df.iloc[0]['Résumé Bart']

    # Remplacer les valeurs manquantes par une chaîne vide
    if pd.isna(resume_bart_column):
        resume_bart_column = ''

    # Renvoyer la valeur de resume_bart_column en tant que chaîne de caractères
    return resume_bart_column

# Appeler la fonction et afficher le résultat
summary = extract_summary_bart()
print(summary)

