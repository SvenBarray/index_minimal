import json
from nltk.tokenize import word_tokenize
import pandas as pd

def load_json_data(filepath):
    """Fonction pour charger les données JSON"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_texts(texts):
    """Fonction pour tokeniser les textes"""
    return [word_tokenize(text) for text in texts]

def calculate_token_statistics(tokens):
    """Fonction pour calculer les statistiques des tokens"""
    total_tokens = sum(len(t) for t in tokens)
    average_tokens = total_tokens / len(tokens)
    return total_tokens, average_tokens

def display_statistics(data, titles_tokens, fields_stats=False):
    """
    Fonction pour afficher les statistiques de nos données. 
    Il y a une redondance des paramètres avec titles_tokens (issus de data), mais cela permet d'éviter de tokéniser les titres deux fois.
    field_stats détermine si on veut également les statistiques du contenu et des headers. Si False, on aura seulement les données des titres. False par défaut car cette opération est coûteuse en temps
    """
    total_tokens_titles, avg_tokens_titles = calculate_token_statistics(titles_tokens)

    num_documents = len(data)
    df = pd.DataFrame({'TitleTokens': [len(t) for t in titles_tokens]})


    if fields_stats:
        contents = [doc['content'] for doc in data]
        headers = [doc['h1'] for doc in data]
        contents_tokens = tokenize_texts(contents)
        headers_tokens = tokenize_texts(headers)
        total_tokens_contents, avg_tokens_contents = calculate_token_statistics(contents_tokens)
        total_tokens_headers, avg_tokens_headers = calculate_token_statistics(headers_tokens)
        total_global_tokens = total_tokens_titles + total_tokens_contents + total_tokens_headers
        avg_global_tokens = total_global_tokens / num_documents
        df['ContentTokens'] = [len(t) for t in contents_tokens]
        df['HeaderTokens'] = [len(t) for t in headers_tokens]
        print(f"Nombre de documents : {num_documents}")
        print(f"Nombre total de tokens : {total_global_tokens}")
        print(f"Nombre de tokens moyen par document : {avg_global_tokens}\n")
        print(f"Nombre de tokens de titres : {total_tokens_titles}")
        print(f"Nombre de tokens de titres moyen par document : {avg_tokens_titles}\n")
        print(f"Nombre de tokens de contenu : {total_tokens_contents}")
        print(f"Nombre de tokens de titres moyen par document : {avg_tokens_contents}\n")
        print(f"Nombre de tokens h1 : {total_tokens_headers}")
        print(f"Nombre de tokens de titres moyen par document : {avg_tokens_headers}\n")
    else:
        print(f"Nombre de documents : {num_documents}\n")
        print(f"Nombre de tokens de titre : {total_tokens_titles}")
        print(f"Nombre de tokens de titres moyen par document : {avg_tokens_titles}\n")
    print(f"Distribution des tokens :")
    print(df.describe())

if __name__ == "__main__":
    path = 'crawled_urls.json'
    data = load_json_data(path)
    titles = [doc['title'] for doc in data]
    titles_tokens = tokenize_texts(titles)
    display_statistics(data, titles_tokens, fields_stats=False)