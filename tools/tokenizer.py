from nltk.tokenize import word_tokenize

def tokenize_texts(texts):
    """Tokenise une liste de textes en une liste de listes de tokens."""
    return list(map(word_tokenize, texts))