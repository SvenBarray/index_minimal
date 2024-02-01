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
    return [word_tokenize(text) for text in texts]

def calculate_token_statistics(tokens):
    """Fonction pour calculer les statistiques des tokens"""
    total_tokens = sum(len(t) for t in tokens)
    average_tokens = total_tokens / len(tokens)
    return total_tokens, average_tokens

def calculate_statistics(data, titles_tokens, fields_stats=True, extract_metadata=True):
    """
    Fonction pour afficher les statistiques de nos données
    Il y a une redondance des paramètres avec titles_tokens (issus de data), mais cela permet d'éviter de tokeniser les titres deux fois

    field_stats: détermine si on veut également les statistiques du contenu et des headers. Si False, on aura seulement les données des titres. L'option est proposée car cette opération est coûteuse en temps
    extract_metadata: détermine si on extrait les statistiques calculées en tant que metadonnées dans un fichier metadata.json
    """
    num_documents = len(data)

    total_tokens_titles, avg_tokens_titles = calculate_token_statistics(titles_tokens)
    titles_unique_tokens = len(set([token for sublist in titles_tokens for token in sublist]))
    titles_lexical_diversity = titles_unique_tokens / total_tokens_titles if total_tokens_titles else 0
    df = pd.DataFrame({'TitleTokens': [len(t) for t in titles_tokens]})

    statistics = {
        'global': {'total_documents': num_documents},
        'titles': {
            'total_tokens': total_tokens_titles,
            'avg_tokens_per_document': avg_tokens_titles,
            'unique_tokens': titles_unique_tokens,
            'lexical_diversity': titles_lexical_diversity
        }
    }

    if fields_stats:
        contents = [doc['content'] for doc in data]
        contents_tokens = tokenize_texts(contents)
        total_tokens_contents, avg_tokens_contents = calculate_token_statistics(contents_tokens)
        contents_unique_tokens = len(set([token for sublist in contents_tokens for token in sublist]))
        contents_lexical_diversity = contents_unique_tokens / total_tokens_contents if total_tokens_contents else 0
        df['ContentTokens'] = [len(t) for t in contents_tokens]

        headers = [doc['h1'] for doc in data]
        headers_tokens = tokenize_texts(headers)
        total_tokens_headers, avg_tokens_headers = calculate_token_statistics(headers_tokens)
        headers_unique_tokens = len(set([token for sublist in headers_tokens for token in sublist]))
        headers_lexical_diversity = headers_unique_tokens / total_tokens_headers if total_tokens_headers else 0
        df['HeaderTokens'] = [len(t) for t in headers_tokens]

        total_global_tokens = total_tokens_titles + total_tokens_contents + total_tokens_headers
        avg_global_tokens = total_global_tokens / num_documents


        statistics['global'].update({
            'total_tokens': total_global_tokens,
            'avg_tokens_per_document': avg_global_tokens
        })
        statistics['contents'] = {
            'total_tokens': total_tokens_contents,
            'avg_tokens_per_document': avg_tokens_contents,
            'unique_tokens': contents_unique_tokens,
            'lexical_diversity': contents_lexical_diversity
        }
        statistics['headers'] = {
            'total_tokens': total_tokens_headers,
            'avg_tokens_per_document': avg_tokens_headers,
            'unique_tokens': headers_unique_tokens,
            'lexical_diversity': headers_lexical_diversity
        }

    print("Statistiques sur les données :")
    print(json.dumps(statistics, indent=2))

    if extract_metadata:
        save_metadata_to_file(statistics, 'metadata.json')
        print("Les statistiques ont été extraites avec succès en tant que metadonnées dans le fichier metadata.json.")

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

    titles = [doc['title'] for doc in data]
    titles_tokens = tokenize_texts(titles)

    # Calculer des statistiques sur nos données et les extraire en tant que métadonnées
    calculate_statistics(data, titles_tokens, fields_stats=False, extract_metadata=True)

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