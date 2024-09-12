# minesweeper

Exercice : Création d'un jeu de démineur en Python

## Objectif

Développer une version du jeu classique du démineur en Python, avec une interface graphique.

## Description

Créez une application qui simule le jeu du démineur. Le jeu doit générer une grille avec des mines cachées, et permettre au joueur de révéler des cases en évitant les mines.

## Fonctionnalités requises

1. Génération du plateau
Créer une grille de taille paramétrable (par exemple, 9x9, 16x16, 30x16)
Placer aléatoirement un nombre défini de mines sur la grille

2. Interface graphique
Afficher la grille sous forme de boutons cliquables
Permettre un clic gauche pour révéler une case
Permettre un clic droit pour marquer/démarquer une mine supposée

3. Logique du jeu
Révéler le nombre de mines adjacentes lorsqu'une case est cliquée
Si une case sans mines adjacentes est révélée, révéler automatiquement les cases voisines
Terminer le jeu si une mine est cliquée (défaite)
Vérifier la victoire lorsque toutes les cases non-minées sont révélées

4. Fonctionnalités supplémentaires
Afficher un compteur de mines restantes
Implémenter un chronomètre
Permettre de choisir la difficulté (débutant, intermédiaire, expert) qui ajuste la taille de la grille et le nombre de mines

## Bonus

Ajouter des effets sonores
Implémenter une fonctionnalité de sauvegarde/chargement de partie
Créer un tableau des meilleurs scores

## Contraintes techniques

Utiliser la programmation orientée objet
Implémenter une séparation claire entre la logique du jeu et l'interface graphique
Gérer efficacement les événements de la souris

## Installation

1. **Créer un environnement virtuel**:

   ```sh
   python -m venv venv
   ```

2. **Activer l'environnement virtuel**:

   - Sous Windows:

     ```sh
     venv\Scripts\activate
     ```

   - Sous macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

3. **Installer les dépendences**:

   ```sh
   pip install -r requirements.txt
   ```

## Utilisation

1. **Exécuter l'application**:

   ```sh
   python src/main.py
   ```