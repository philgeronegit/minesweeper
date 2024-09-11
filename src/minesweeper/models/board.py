# model/board.py

import random
from model.cell import Cell

class Board:
    DIFFICULTY_LEVELS = {
        'easy': {'x_size': 9, 'y_size': 9, 'mines': 5},
        'medium': {'x_size': 16, 'y_size': 16, 'mines': 40},
        'hard': {'x_size': 30, 'y_size': 16, 'mines': 80}
    }


# Initializes the board with dimensions and number of mines.

    def __init__(self, x_size, y_size, mines, difficulty="easy"):
        self.x_size = x_size                # Number of columns
        self.y_size = y_size                # Number of rows
        self.mines = mines                  # Number of mines
        self.flags = 0                      # Number of flags placed
        self.cells = [[Cell() for _ in range(y_size)] for _ in range(x_size)]  # Grid of cells
        self.difficulty = difficulty        # Difficulty level
        self.generate_mines()               # Random placement of mines
        self._calculate_adjacent_mines()    # Calculate adjacent mines for each cell


# Initializes the board based on the difficulty level.

    @classmethod
    def from_difficulty(cls, difficulty):
        match difficulty:
            case 'easy' | 'medium' | 'hard':
                config = cls.DIFFICULTY_LEVELS[difficulty]
                return cls(config['x_size'], config['y_size'], config['mines'], difficulty)
            case _:
                raise ValueError(f"Unknown difficulty level '{difficulty}'")

# Randomly places mines on the board.

    def generate_mines(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            x, y = random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1)
            if not self.cells[x][y].is_mine:
                self.cells[x][y].is_mine = True
                mine_positions.add((x, y))

# Calculates the number of adjacent mines for each non-mined cell.

    def _calculate_adjacent_mines(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].adjacent_mine = self._count_adjacent_mines(x, y)

#Counts the mines adjacent to the specified cell.

    def _count_adjacent_mines(self, x, y):
        adjacent_positions = [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)
                              if 0 <= i < self.x_size and 0 <= j < self.y_size and (i, j) != (x, y)]
        return sum(self.cells[i][j].is_mine for i, j in adjacent_positions)

# Adds or removes a flag on the specified cell.

    def set_flag(self, x, y):
        cell = self.cells[x][y]
        match (cell.is_opened, cell.is_flagged):
            case (True, _):
                return  # Cannot flag an already opened cell
            case (False, True):
                cell.is_flagged = False
                self.flags -= 1
            case (False, False):
                cell.is_flagged = True
                self.flags += 1


#Reveals the specified cell and adjacent cells if it has no nearby mines.
        
    def reveal_cells(self, x, y):
        cell = self.cells[x][y]
        if cell.is_opened or cell.is_flagged:
            return
        cell.is_opened = True
        if cell.adjacent_mine == 0 and not cell.is_mine:
            adjacent_positions = [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)
                                  if 0 <= i < self.x_size and 0 <= j < self.y_size and (i, j) != (x, y)]
            for i, j in adjacent_positions:
                self.reveal_cells(i, j)

# Checks if all non-mined cells have been revealed (win condition).

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_opened:
                    return False
        return True
