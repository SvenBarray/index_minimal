import json

def save_metadata_to_file(metadata, path):
    """Enregistre les métadonnées dans un fichier JSON."""
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False)

def save_index_to_file(index, path):
    """Enregistre l'index dans un fichier JSON."""
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(index, file, ensure_ascii=False)