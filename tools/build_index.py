from nltk.stem import PorterStemmer

def build_index(tokens_list, stem_tokens=False, positional=False):
    """
    Construit un index, positionnel ou non positionnel, avec ou sans stemming des tokens.

    Args:
        tokens_list (list): Une liste de listes de tokens.
        positional (bool, optional): False par défaut. Indique si un index positionnel doit être construit.
        stem_tokens (bool, optional): False par défaut. Indique si le stemming doit être appliqué aux tokens.
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