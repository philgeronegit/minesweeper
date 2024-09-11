import time
from minesweeper.models.board import Board

# Here we initialize the game status based on the difficulty level
class GameState:
    def __init__(self, board):
        self.board = board
        self.start_time = None  # Time to start the game
        self.win_time = None    # Indicate how many time the player put to win
        self.game_over = False  # Indicate the end of the game
        self.game_won = False   # Indicate whether the player won the game

    # Starts the game and initializes the timer.
    def start_game(self):
        self.start_time = time.time()
        self.game_over = False
        self.game_won = False
        self.win_time = None

    # Check if the game is over.
    def is_game_over(self):
        return self.game_over

    # Check if the player won the game.
    def is_game_won(self):
        return self.game_won

    # Reveals the cell, and checks if it's a mine or a safe cell.
    def reveal_cell(self, x, y):
        cell = self.board.cells[x][y]
        if cell.is_mine:
            self.game_over = True
            return 'X'
        else:
            return cell.reveal()

    # Check if the player has won the game.
    def check_victory(self):
        if self.board.check_win():
            self.game_over = True
            self.game_won = True
            self.win_time = time.time()  # Records the time when the victory is achieved
            return True
        return False

    # Returns game duration in seconds.
    def get_game_duration(self):
        if self.start_time is None:
            return 0
        if self.game_won and self.win_time is not None:
            return self.win_time - self.start_time  # Duration until the victory
        return time.time() - self.start_time  # Duration since the game started

    # Returns the number of remaining mines.
    def get_remaining_mines(self):
        return self.board.mines - self.board.flags