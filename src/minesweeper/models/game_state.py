import time
from minesweeper.models.board import Board, EASY_DIFFICULTY
from minesweeper.models.persistence import JsonPersistence


class GameState:
    def __init__(self, board: Board = None, difficulty: str = EASY_DIFFICULTY):
        self._board = board if board is not None else Board(difficulty)
        self.start_time = None  # Time to start the game
        self.won_time = None  # Indicate how many time the player put to win
        self.game_over = False  # Indicate the end of the game
        self.game_won = False  # Indicate whether the player won the game
        self.best_scores = []
        self.score_added = False
        self.first_cell_revealed = False
        self.persistence = JsonPersistence()
        print(f"Game state created with difficulty {difficulty}")
        if self.persistence.is_file_exists():
            self.best_scores = self.persistence.load()

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
        return GameStateDTO(self)

    # Reset the game and initializes the timer.
    def reset(self):
        self.start_time = None
        self.game_over = False
        self.game_won = False
        self.score_added = False
        self.first_cell_revealed = False
        self._board.generate_mines()

    def start_timer(self):
        self.start_time = time.time()
        self.first_cell_revealed = True

    # Reveals the cell, and checks if it's a mine or a safe cell.
    def reveal_cell(self, x, y):
        cell = self._board.cells[x][y]
        if cell.is_mine:
            self.game_over = True
            return "X"
        else:
            return cell.reveal()

    # Check if the player has won the game.
    def check_victory(self):
        if self._board.check_win():
            self.won_time = self.ellapsed_time
            self.game_won = True

            if not self.score_added:
                self.score_added = True
                self.best_scores.append(self.ellapsed_time)
                self.best_scores.sort()
                if len(self.best_scores) > 5:
                    self.best_scores.pop()
                print(f"Best scores: {self.best_scores}")
                self.persistence.dump(self.best_scores)

            return True
        return False

    # Returns game ellapsed time.
    @property
    def ellapsed_time(self):
        if self.start_time is None:
            return "00:00"

        if not self.game_over and not self.game_won:
            ellapsed_time = time.time() - self.start_time
            self.minutes = int(ellapsed_time // 60)
            self.seconds = int(ellapsed_time % 60)
        return f"{self.minutes:02}:{self.seconds:02}"

    # Returns the number of remaining mines.
    def get_remaining_mines(self):
        return self._board.mines_count - self._board.flags


class GameStateDTO:
    """Data Transfer Object for the game state"""

    def __init__(self, game_state: GameState):
        self.cells = game_state.cells
        self.difficulty = game_state.difficulty
        self.mines = game_state.mines
        self.game_over = game_state.game_over
        self.first_cell_revealed = game_state.first_cell_revealed
