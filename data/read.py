import json

def load_json_data(filepath):
    """Charge les données à partir d'un fichier JSON."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)
