# content.py
import sys

def process_content_options(args):
    # Construire une chaîne de résumé des options choisies
    return f"Type: {args[0]}, Emojis: {args[1]}, Image: {args[2]}, Sign: {args[3]}"

if __name__ == "__main__":
    # Les arguments sont passés directement
    options_summary = process_content_options(sys.argv[1:])
    print(options_summary)  # On imprime le résumé qui sera capturé par subprocess
