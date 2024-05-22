from openai import OpenAI
import recovery_summary

OPENAI_API_KEY = '<secret_key>'

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_responses(prompts):
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
        chat = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages)     # temperature=1 et n=1

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
    print("-----\n")
    tweet = responses[-1]
    print(tweet)
    
    # return responses


if __name__ == "__main__":
    # Ouverture des fichiers texte
    with open('INGE2-X-Project/Prompt/debut.txt', 'r') as f:
        text = f.read()
    with open('INGE2-X-Project/Prompt/suite_1.txt', 'r') as g:
        text_1 = g.read()
    with open('INGE2-X-Project/Prompt/suite_2.txt', 'r') as h:
        text_2 = h.read()
    with open('INGE2-X-Project/Prompt/suite_1_emoji.txt', 'r') as j:
        text_1_emoji = j.read()
    with open('INGE2-X-Project/Prompt/suite_2_emoji.txt', 'r') as k:
        text_2_emoji = k.read()
    with open('INGE2-X-Project/Prompt/suite_1_long.txt', 'r') as j:
        text_1_long = j.read()
    with open('INGE2-X-Project/Prompt/suite_2_long.txt', 'r') as k:
        text_2_long = k.read()
    with open('INGE2-X-Project/Prompt/suite_1_thread.txt', 'r') as j:
        text_1_thread = j.read()
    with open('INGE2-X-Project/Prompt/suite_2_thread.txt', 'r') as k:
        text_2_thread = k.read()

    # Génération du résumé
    summary = recovery_summary.extract_summary_bart()
    prompt_input_3 = text_2 + "\n\n" + summary + "\n\n"
    prompt_input_4 = text_2_emoji + "\n\n" + summary + "\n\n"
    prompt_input_5 = text_2_long + "\n\n" + summary + "\n\n"
    prompt_input_6 = text_2_thread + "\n\n" + summary + "\n\n"

    # Création des listes de prompts
    prompts = [text, text_1, prompt_input_3]
    prompts_emoji = [text, text_1_emoji, prompt_input_4]
    prompts_long = [text, text_1_long, prompt_input_5]
    prompts_thread = [text, text_1_thread, prompt_input_6]

    # Sélection du type de tweet
choix = input("si vous voulez un tweet avec emoji tapez (2) si vous voulez un tweet long tapez (3), si vous voulez un tweet thread tapez (4) :")

if choix == "1":
    generate_responses(prompts)
elif choix == "2":
    generate_responses(prompts_emoji)
elif choix == "3":
    generate_responses(prompts_long)
elif choix == "4":
    generate_responses(prompts_thread)
else:
    print("Choix invalide. Veuillez choisir 1, 2, 3 ou 4.")


