import pandas as pd
import requests
from PIL import Image

# Clés API
HF_API_KEY_SD = "API_KEY"
HF_API_KEY_LL = "API_KEY"

# URL des API
SD_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
LL_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

# Fonction pour interroger l'API pour améliorer le prompt
def improve_prompt(text):
    headers = {"Authorization": f"Bearer {HF_API_KEY_LL}"}
    payload = {"inputs": f"Generate a detailed image prompt for the following description: {text}"}
    response = requests.post(LL_API_URL, headers=headers, json=payload)
    response_json = response.json()
    
    # Vérifiez la structure de la réponse JSON
    if isinstance(response_json, list) and len(response_json) > 0:
        improved_text = response_json[0].get('generated_text', text).strip()  # Accédez au premier élément de la liste
    else:
        improved_text = text  # Si la réponse n'est pas conforme, utilisez le texte original

    return improved_text

# Fonction pour interroger l'API pour générer une image à partir du texte
def generate_image_from_text(text):
    headers = {"Authorization": f"Bearer {HF_API_KEY_SD}"}
    payload = {"inputs": text}
    response = requests.post(SD_API_URL, headers=headers, json=payload)
    image_bytes = response.content
    return image_bytes

# Charger le fichier CSV contenant les articles
def load_csv(file_path):
    return pd.read_csv(file_path, delimiter=';')
def main():
    df = load_csv('choix_tendances_tags.csv')

    for index, row in df.iterrows():
        text = row['Titre']
        improved_text = improve_prompt(text)
        print(improved_text)
        image_bytes = generate_image_from_text(improved_text)

        image_path = f"image_article_{index}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)

if __name__ == "__main__":
    main()
