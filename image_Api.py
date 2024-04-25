import pandas as pd
import requests
import io
from PIL import Image

# Fonction pour interroger l'API pour générer une image à partir du texte
def generate_image_from_text(text):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content
    return image_bytes

# Charger le fichier CSV contenant les articles
df = pd.read_csv('choix_tendances_tags.csv', delimiter=';')

# Itérer à travers chaque ligne du fichier CSV
for index, row in df.iterrows():
    # Récupérer le texte de l'article
    text = row['description']
    # Générer l'image à partir du texte
    image_bytes = generate_image_from_text(text)
    
    # Enregistrer l'image avec un nom unique (par exemple, l'index de la ligne)
    image_path = f"image_{index}.png"
    with open(image_path, "wb") as f:
        f.write(image_bytes)
