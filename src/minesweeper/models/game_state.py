import time
from minesweeper.models.board import Board, EASY_DIFFICULTY

class GameStateDTO:
    """Data Transfer Object for the game state"""
    def __init__(self, cells, difficulty, mines, game_over):
        self.cells = cells
        self.difficulty = difficulty
        self.mines = mines
        self.game_over = game_over

# Here we initialize the game status based on the difficulty level
class GameState:
    def __init__(self, board: Board = None, difficulty: str = EASY_DIFFICULTY):
        self._board = board if board is not None else Board(difficulty)
        self.start_time = None  # Time to start the game
        self.won_time = None    # Indicate how many time the player put to win
        self.game_over = False  # Indicate the end of the game
        self.game_won = False   # Indicate whether the player won the game
        self.best_scores = ["30s", "40s", "50s"]
        print(f"Game state created with difficulty {difficulty}")

    @property 
    def cells(self):
        return self._board.cells

    @property
    def difficulty(self):
        return self._board.difficulty

    @property
    def mines(self):
        return self._board.mines

    def get_data(self):
        return GameStateDTO(self.cells, self.difficulty, self.mines, self.game_over)

    # Reset the game and initializes the timer.
    def reset(self):
        self.start_time = time.time()
        self.game_over = False
        self.game_won = False
        self._board.generate_mines()

    # Reveals the cell, and checks if it's a mine or a safe cell.
    def reveal_cell(self, x, y):
        cell = self._board.cells[x][y]
        if cell.is_mine:
            self.game_over = True
            return 'X'
        else:
            return cell.reveal()

    # Check if the player has won the game.
    def check_victory(self):
        if self._board.check_win():
            self.game_won = True
            self.won_time = time.time()  # Records the time when the victory is achieved
            return True
        return False

    # Returns game ellapsed time.
    @property
    def ellapsed_time(self):
        if self.start_time is None:
            return "00:00"

        if not self.game_over and not self.game_won:
            ellapsed_time = time.time() - self.start_time
            minutes = int(ellapsed_time // 60)
            seconds = int(ellapsed_time % 60)
            return f"{minutes:02}:{seconds:02}"

    # Returns the number of remaining mines.
    def get_remaining_mines(self):
        return self._board.mines_count - self._board.flags