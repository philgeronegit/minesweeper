import time
from model.board import Board

class GameState:
    def __init__(self, difficulty="easy"):
        """
        Initialise l'état du jeu en fonction de la difficulté choisie.
        """
        self.board = Board.from_difficulty(difficulty)  # Le plateau du jeu
        self.start_time = None  # Temps auquel le jeu commence
        self.win_time = None    # Temps auquel le jeu a été gagné (si applicable)
        self.game_over = False  # Indicateur de fin de partie
        self.game_won = False   # Indicateur de victoire