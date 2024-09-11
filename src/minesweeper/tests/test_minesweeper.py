import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../model')))

import pytest
from model.cell import Cell
from model.board import Board
from model.gamestate import GameState

@pytest.fixture
def easy_game():
    """
    Fixture to initialize a 3x3 game with difficulty 'easy'.
    """
    board = Board(x_size=3, y_size=3, mines=3, difficulty="easy")
    game_state = GameState(board)
    return game_state

def test_board_initialization(easy_game):
    """
    Test if the board initializes correctly with the right size and number of mines.
    """
    assert easy_game.board.x_size == 3
    assert easy_game.board.y_size == 3
    assert easy_game.board.mines == 3
    assert sum([1 for row in easy_game.board.cells for cell in row if cell.is_mine]) == 3

def test_cell_flagging(easy_game):
    """
    Test flagging functionality of the cells.
    """
    easy_game.board.set_flag(0, 0)
    assert easy_game.board.cells[0][0].is_flagged is True
    easy_game.board.set_flag(0, 0)
    assert easy_game.board.cells[0][0].is_flagged is False

def test_game_loss_on_mine_reveal(easy_game):
    """
    Test if revealing a mine ends the game.
    """
    for x in range(3):
        for y in range(3):
            if easy_game.board.cells[x][y].is_mine:
                result = easy_game.reveal_cell(x, y)
                assert result is True  # Game should end as it's a mine
                assert easy_game.game_over is True
                return

def test_game_win(easy_game):
    """
    Test winning the game by revealing all non-mined cells.
    """
    for x in range(3):
        for y in range(3):
            if not easy_game.board.cells[x][y].is_mine:
                easy_game.reveal_cell(x, y)

    assert easy_game.check_victory() is True
    assert easy_game.game_won is True
