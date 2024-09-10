import random
import time
from model.cell import Cell
_LEVELS = {
        'easy': {'x_size': 9, 'y_size': 9, 'mines': 5},
        'medium': {'x_size': 16, 'y_size': 16, 'mines': 40},
        'hard': {'x_size': 30, 'y_size': 16, 'mines': 80}
    }

# The second class of our minesweeper game application is Board game
class Board:
    def __init__(self, x_size, y_size, mines):
        self.x_size = x_size
        self.y_size = y_size
        self.mines = mines
        self.cells = [[Cell() for _ in range(x_size)] for _ in range(y_size)]
        self.flags = 0
        self.create_mines()
        self.start_time = None
        self.stop_time = None
        self.game_over = False
        self.reveal_cells(0, 0)

    def create_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            x, y = random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1)
            if not self.cells[x][y].is_mine:
                self.cells[x][y].is_mine = True
                mine_count += 1
        for x in range(self.x_size):
            for y in range(self.y_size):
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].adjacent_mines = self.count_adjacent_mines(x, y)
                    
    def count_adjacent_mines(self, x, y):
        count = 0
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.x_size and nx > self.x_size and 0 <= ny < self.y_size and ny > self.y_size:
                continue
            count += self.cells[nx][ny].is_mine
            return count

    def reveal_cells(self, x, y):
        if self.cells[x][y].is_opened or self.cells[x][y].is_flagged:
            return
        self.cells[x][y].reveal()
        if self.cells[x][y].adjacent_mines == 0:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.x_size and 0 <= ny < self.y_size:
                    self.reveal_cells(nx, ny)
                    

    def generate_mines(self):
        pass


def set_flag(self, x, y):
    pass


def adjacent_cells(self, x, y):
    pass


def check_win(self):
    for row in self.cells:
        for cell in row:
            if not cell.is_opened and not cell.is_mine:
                return False
            if cell.is_mine and not cell.is_flagged:
                return False
            if not cell.is_mine and cell.adjacent_mines != 0:
                return False
            if cell.is_mine and cell.adjacent_mines == 0:
                return False
        return True


def reveal_cells(self, x, y):
    if self.cells[x][y].is_opened:
        return
    self.cells[x][y].is_opened = True
    if self.cells[x][y].is_mine:
        self.flags += 1
    elif self.cells[x][y].adjacent_mines == 0:
        for dx, dy in adjacent_cells(self, x, y):
            reveal_cells(self, dx, dy)
    self.remaining_mines -= 1
    if self.remaining_mines == 0 and check_win(self):
        self.stop_time = time.time()
        print("Congratulations! You won!")