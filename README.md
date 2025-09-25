# MGP2-DataScienceProj

Exercice: Créer une entreprise fictive ou prendre une existante et imaginer un projet de Data Science pour cette entreprise.

## Sujet : Analyse des données musicales pour trouver des tendances et des opportunités de marché.

### Contexte
On est une entreprise spécialisée dans le consulting en analyse de données. Pour aider des labels internationaux et locaux (aux US) à mieux target ces 2 marchés, on a décidé de se pencher sur les données musicales disponibles publiquement pour en extraire des tendances et des opportunités de marché.

## Jeu de Données

On a décidé d'utiliser les données de Spotify et Billboard pour notre analyse. On a donc récupéré les données suivantes :
https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs
https://www.kaggle.com/datasets/josephinelsy/spotify-top-hit-playlist-2010-2022

## Objectifs

Répondre à 3 problématiques business :
Comment organiser son plan marketing par rapport à la durée de vie d'un hit ?
Y a-t-il une disparité entre les hits aux US et les hits internationaux ? Quelles sont les genres qui marchent le mieux dans les 2 cas ?
Quelles sont les caractéristiques audio les plus présentes dans les hits ? Y a-t-il des caractéristiques communes entre les hits aux US et les hits internationaux ?

## Organisation des fichiers
Le jupyter notebook utilisé pour nettoyer les données est `songs-preprocessing.ipynb`. Ce préprocessing doit être fait avant d'exécuter le dashboard car les datasets nettoyés ne sont pas inclus dans le repo.
Le jupyter notebook utilisé pour l'analyse des données est `songs-vis.ipynb`.
Le dashboard est dans `website.py`.
Les datasets originaux sont dans le dossier `dataset/`.
Les datasets nettoyés sont dans le dossier `cleaned_dataset/`.
La présentation se trouve dans le dossier `docs/`.