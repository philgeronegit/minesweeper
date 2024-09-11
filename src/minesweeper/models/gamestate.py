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

    def start_game(self):
        self.start_time = time.time()
        self.game_over = False
        self.game_won = False
        self.win_time = None
        

# Here we update the game status based on user input

    def is_game_over(self):
        return self.game_over
    
    def is_game_won(self):
        return self.game_won


# The reveal function reveal the cell, check it safety  and check the click on a mine.
# If the player clicks on a mine then the game is over and if not the adjacent celles are revealed

    def reveal_cell(self, x, y):
        if self.game_over:
            return
        cell = self.board.cells[x][y]
        match cell.is_mine:
            case True:
                self.game_over = True
                return True
            case False:
                self.board.reveal_cells(x, y)
                return False

