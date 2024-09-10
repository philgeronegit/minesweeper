'''we are going to write the script for the application minesweeper game. The game must generate a grid with hidden mines, and allow the player to reveal squares by avoiding the mines.
Here are the required functionnalities:
1. Tray generation
Create a grid of configurable size (e.g. 9x9 with 5 mines, 16x16 with 40 mines, 30x16 with 80 mines)
Randomly place a defined number of mines on the grid
2. Graphic interface
Display grid as clickable buttons
Left-click to reveal a cell
Right-click to mark/start a preset mine
3. Game logic
Reveal the number of adjacent mines when a square is clicked.
If a square with no adjacent mines is revealed, automatically reveal neighboring squares
End the game if a mine is clicked (defeat)
Check for victory when all unmined squares are revealed
4. Additional features
Display a remaining mine counter
Implement a stopwatch
Select difficulty (beginner, intermediate, expert) which adjusts grid size and number of mines''' 

# The first class of our minesweeper game application is Cell

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_opened = False
        self.is_flagged = False
        self.adjacent_mines = 0


# the function reveal will help us determine wether or not a mine or a case is discovered
    def reveal(self):
        self.is_opened = True
        if self.is_mine:
            return 'X'
        elif self.adjacent_mines == 0:
            return ' '
        else:
            return str(self.adjacent_mines)


# display for easy debugging
    def __repr__(self):
        if self.is_flagged:
            return "F"
        elif not self.is_opened:
            return "C"
        elif self.is_mine:
            return "M"
        else:
            return str(self.adjacent_mine)

