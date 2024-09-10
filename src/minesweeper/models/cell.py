# The first class of our minesweeper game application is Cell
# initialize a cell with default attributes

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_opened = False
        self.is_flagged = False
        self.adjacent_mines = 0


# display for easy debugging
    def __repr__(self):
        if self.is_flagged:
            return "F"
        elif not self.is_opened:
            return "C"
        elif self.is_mine:
            return "M"
        elif self.adjacent_mine > 0:
            return str(self.adjacent_mine)
        else:
            return " "

# the function reveal will help us determine wether or not a mine or a case is discovered
# Reveals the cell and returns a symbol based on its content.
# 'X' for mines, ' ' for empty cells, and the number of adjacent mines otherwise.

    def reveal(self):
        self.is_opened = True
        if self.is_mine:
            return 'X'
        elif self.adjacent_mines == 0:
            return ' '
        else:
            return str(self.adjacent_mines)