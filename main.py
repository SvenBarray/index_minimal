from data.read import load_json_data
from data.write import save_index_to_file
from tools.tokenizer import tokenize_texts
from tools.statistics import calculate_statistics
from tools.build_index import build_index

if __name__ == "__main__":
    path = 'data/input/crawled_urls.json'
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
    save_index_to_file(non_pos_index, 'data/output/title.non_pos_index.json')

    # Construire et sauvegarder un index non positionnel avec stemming
    stemmed_non_pos_index = build_index(titles_tokens, stem_tokens=True, positional=False)
    save_index_to_file(stemmed_non_pos_index, 'data/output/stemmed_title.non_pos_index.json')

    # Construire et sauvegarder un index positionnel sans stemming
    positional_index = build_index(titles_tokens, stem_tokens=False, positional=True)
    save_index_to_file(positional_index, 'data/output/title.pos_index.json')

    # Construire et sauvegarder un index positionnel avec stemming pour les headers
    stemmed_headers_positional_index = build_index(headers_tokens, stem_tokens=True, positional=True)
    save_index_to_file(stemmed_headers_positional_index, 'data/output/stemmed_headers.pos_index.json')