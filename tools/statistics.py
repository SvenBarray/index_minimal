import json
from data.write import save_metadata_to_file

def calculate_statistics(token_dict, extract_metadata=True):
    """
    Calcule les statistiques pour un dictionnaire de listes de tokens.

    Args:
        token_dict (dict): Un dictionnaire contenant des listes de tokens, chaque clé représentant une catégorie.
        extract_metadata (bool, optional): True par défaut. Indique si les statistiques doivent être extraites en tant que métadonnées dans un fichier.
    """
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
        save_metadata_to_file(statistics, 'data/output/metadata.json')

def calculate_text_statistics(tokens_list):
    """Calcule les statistiques pour une liste de tokens."""
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