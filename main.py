import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pandas as pd

def load_json_data(filepath):
    """Fonction pour charger les données JSON"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_texts(texts):
    """Fonction pour tokeniser les textes"""
    return list(map(word_tokenize, texts))

def calculate_token_statistics(tokens):
    """Fonction pour calculer les statistiques des tokens"""
    total_tokens = sum(len(t) for t in tokens)
    average_tokens = total_tokens / len(tokens)
    return total_tokens, average_tokens

def calculate_statistics(token_dict, extract_metadata=True):
    """Calculer les statistiques pour un dictionnaire de listes de tokens."""
    statistics = {}
    all_tokens = []

    # Calculer le nombre total de documents pour la première clé disponible dans token_dict
    nb_documents = len(token_dict[next(iter(token_dict))] if token_dict else 0)
    statistics['global'] = {'total_documents': nb_documents}

    # Fusionner tous les tokens pour le calcul global
    for tokens_list in token_dict.values():
        all_tokens.extend(tokens_list)

    # Ajouter les statistiques globales (à l'exception de total_documents déjà ajouté)
    global_stats = calculate_text_statistics(all_tokens)
    global_stats.pop('nb_documents', None)  # Retirer total_documents si présent
    statistics['global'].update(global_stats)

    # Calculer les statistiques pour chaque catégorie de tokens
    for key, tokens_list in token_dict.items():
        statistics[key] = calculate_text_statistics(tokens_list)

    print("Statistiques sur les données :")
    print(json.dumps(statistics, indent=2))

    # Extraire les statistiques en tant que metadata
    if extract_metadata:
        save_metadata_to_file(statistics, 'metadata.json')
        print("Les statistiques ont été extraites avec succès en tant que metadonnées dans le fichier metadata.json.")

def calculate_text_statistics(tokens_list):
    """Calculer et retourner les statistiques pour une liste de tokens."""
    total_tokens = sum(len(tokens) for tokens in tokens_list)
    unique_tokens = len(set(token for sublist in tokens_list for token in sublist))
    avg_tokens = total_tokens / len(tokens_list) if tokens_list else 0
    lexical_diversity = unique_tokens / total_tokens if total_tokens else 0

    return {
        'total_tokens': total_tokens,
        'unique_tokens': unique_tokens,
        'avg_tokens_per_document': avg_tokens,
        'lexical_diversity': lexical_diversity
    }

def save_metadata_to_file(metadata, filename):
    """Enregistrement des métadonnées dans un fichier."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False)

def build_index(tokens_list, stem_tokens=False, positional=False):
    """
    Construit un index, positionnel ou non positionnel, avec ou sans stemming des tokens.

    stem_tokens: Si True, applique le stemming aux tokens.
    positional: Si True, construit un index positionnel.
    """
    if stem_tokens:
        stemmer = PorterStemmer()
        tokens_list = [[stemmer.stem(token) for token in tokens] for tokens in tokens_list]

    index = {}
    for doc_id, tokens in enumerate(tokens_list):
        for pos, token in enumerate(tokens):
            if positional:
                if token not in index:
                    index[token] = {}
                if doc_id not in index[token]:
                    index[token][doc_id] = []
                index[token][doc_id].append(pos)
            else:
                if token not in index:
                    index[token] = []
                if doc_id not in index[token]:
                    index[token].append(doc_id)

    return index

def stem_tokens(tokens):
    """Fonction pour appliquer le stemming aux tokens."""
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def save_index_to_file(index, filename):
    """Fonction pour enregistrer l'index dans un fichier."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(index, file, ensure_ascii=False)

if __name__ == "__main__":
    path = 'crawled_urls.json'
    data = load_json_data(path)

    # Tokenisation. Tokeniser les contents est le plus couteux en temps et il est possible de sauter cette étape si on ne veut pas de traitement statistique des contents.
    titles_tokens = tokenize_texts([doc['title'] for doc in data])
    contents_tokens = tokenize_texts([doc['content'] for doc in data])
    headers_tokens = tokenize_texts([doc['h1'] for doc in data])

    # Création d'un dictionnaire dans lequel on met les listes de token que l'on souhaite traiter statistiquement
    token_dict = {
        'titles': titles_tokens,
        'contents': contents_tokens,
        'headers': headers_tokens
    }

    # Calcul des statistiques
    calculate_statistics(token_dict, extract_metadata=True)

    # Construire et sauvegarder un index non positionnel sans stemming
    non_pos_index = build_index(titles_tokens, stem_tokens=False, positional=False)
    save_index_to_file(non_pos_index, 'title.non_pos_index.json')

    # Construire et sauvegarder un index non positionnel avec stemming
    stemmed_non_pos_index = build_index(titles_tokens, stem_tokens=True, positional=False)
    save_index_to_file(stemmed_non_pos_index, 'stemmed_title.non_pos_index.json')

    # Construire et sauvegarder un index positionnel sans stemming
    positional_index = build_index(titles_tokens, stem_tokens=False, positional=True)
    save_index_to_file(positional_index, 'title.pos_index.json')


    # Construire et sauvegarder un index positionnel avec stemming pour les headers
    headers = [doc['h1'] for doc in data]
    headers_tokens = tokenize_texts(headers)
    stemmed_headers_positional_index = build_index(headers_tokens, stem_tokens=True, positional=True)
    save_index_to_file(stemmed_headers_positional_index, 'stemmed_headers.pos_index.json')