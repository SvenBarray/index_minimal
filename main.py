#import nltk
#nltk.download('punkt')


import json
from nltk.tokenize import word_tokenize
import pandas as pd

def load_json_data(filepath):
    """
    Charge les données à partir d'un fichier JSON.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def calculate_token_statistics(texts):
    """
    Calcule le nombre total et la moyenne de tokens pour une liste de textes.
    """
    tokens = [word_tokenize(text) for text in texts]
    total_tokens = sum(len(t) for t in tokens)
    average_tokens = total_tokens / len(texts)
    return total_tokens, average_tokens

# Fonction pour afficher les statistiques
def display_statistics(data, fields_stats=False):
    """
    Affiche les statistiques des données. Le paramètre fields_stats détermine si on souhaite avoir les statistiques des tokens du titre, contenu, et headers si True, ou juste des titres s.
    """

    titles = [doc['title'] for doc in data]
    total_tokens_titles, avg_tokens_titles = calculate_token_statistics(titles)

    num_documents = len(data)
    global_tokens = total_tokens_titles

    if fields_stats: # False par défaut car le temps d'exécution de cette étape et long 
        contents = [doc['content'] for doc in data]
        headers = [doc['h1'] for doc in data]
        total_tokens_contents, avg_tokens_contents = calculate_token_statistics(contents)
        total_tokens_headers, avg_tokens_headers = calculate_token_statistics(headers)
        global_tokens += total_tokens_contents + total_tokens_headers
    else:
        avg_tokens_contents = avg_tokens_headers = 0

    avg_tokens_per_document = global_tokens / num_documents

    print(f"Nombre de documents : {num_documents}")
    print(f"Nombre total de tokens (global) : {global_tokens}")
    if fields_stats:
        print(f"Nombre total de tokens (titres) : {total_tokens_titles}, Moyenne par document : {avg_tokens_titles}")
        print(f"Nombre total de tokens (contenus) : {total_tokens_contents}, Moyenne par document : {avg_tokens_contents}")
        print(f"Nombre total de tokens (h1) : {total_tokens_headers}, Moyenne par document : {avg_tokens_headers}")
    print(f"Moyenne globale de tokens par document : {avg_tokens_per_document}")

    if fields_stats:
        df = pd.DataFrame({
            'TitleTokens': [len(word_tokenize(t)) for t in titles],
            'ContentTokens': [len(word_tokenize(c)) for c in contents],
            'HeaderTokens': [len(word_tokenize(h)) for h in headers]
        })
        print(df.describe())


if __name__ == "__main__":
    # Chemin vers le fichier JSON
    path = 'crawled_urls.json'

    # Exécution des fonctions
    data = load_json_data(path)
    display_statistics(data, fields_stats=False)
