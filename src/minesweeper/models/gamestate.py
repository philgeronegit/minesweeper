import time
from model.board import Board

# Here we initialize the game status based on the difficulty level

class GameState:
    def __init__(self, difficulty="easy"):
        """
        Initialise l'état du jeu en fonction de la difficulté choisie.
        """
        self.board = Board.from_difficulty(difficulty)  
        self.start_time = None  # Time to start the game
        self.win_time = None    # Indicate how many time the player put to win
        self.game_over = False  # Indicate the end of the game
        self.game_won = False   # Indicate whether the player won the party


# Here we start the game and initialize the timer

def start_game():
    game_state = GameState()
    game_state.start_time = time.time()
    return game_state
