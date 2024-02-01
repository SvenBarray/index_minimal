# Projet d'Indexation Web

## Description

Ce projet implémente un système d'indexation web non positionnel, avec des fonctionnalités supplémentaires telles que la création d'index positionnels et l'application de stemming. Il traite les données extraites d'un crawler web, calcule des statistiques sur les tokens et génère divers types d'index.

## Prérequis

- Python 3
- NLTK

## Installation des dépendances et ressources nécéssaires

```bash
pip install nltk
python -m nltk.downloader punkt
```

## Utilisation

Pour exécuter le script principal, naviguez jusqu'au dossier racine du projet et lancez :

```bash
python main.py
```

Cela traitera les données d'entrée, calculera les statistiques, et générera les index comme spécifié dans le script.

## Fonctionnalités

- Tokenisation des titres, contenus, et en-têtes.
- Calcul des statistiques sur les tokens, telles que le nombre total de tokens, la moyenne des tokens par document, la diversité lexicale, etc.
- Génération d'index non positionnels et positionnels, avec ou sans application de stemming.

## Structure du Projet

- `data/`
- `input/` : Contient les fichiers de données d'entrée (ex. `crawled_urls.json`).
- `output/` : Dossier de sortie pour les fichiers générés (metadata et index).
- `read.py` : Fonctions pour la lecture des données.
- `write.py` : Fonctions pour l'écriture des données.
- `tools/`
- `build_index.py` : Fonctions pour construire les index.
- `statistics.py` : Fonctions pour calculer les statistiques des tokens.
- `tokenizer.py` : Fonction pour tokeniser les textes.
- `main.py` : Script principal pour exécuter le projet.

## Auteur

Ce projet a été réalisé par Sven BARRAY dans le cadre d'un cours d'Indexation Web, lors de sa troisième année du cursus ingénieur à l'ENSAI

