import pytest
from minesweeper.models.board import Board, EASY_DIFFICULTY
from minesweeper.models.game_state import GameState

@pytest.fixture
def easy_game():
    """
    Fixture to initialize a 3x3 game with difficulty 'easy'.
    """
    board = Board(difficulty = EASY_DIFFICULTY)
    game_state = GameState(board)
    return game_state

def test_board_initialization(easy_game):
    """
    Test if the board initializes correctly with the right size and number of mines.
    """
    assert easy_game.board.x_size == 9
    assert easy_game.board.y_size == 9
    assert easy_game.board.mines_count == 5

def test_cell_flagging(easy_game):
    """
    Test flagging functionality of the cells.
    """
    easy_game.board.set_flag(0, 0)
    assert easy_game.board.cells[0][0].is_flagged

def test_game_loss_on_mine_reveal(easy_game):
    """
    Test if revealing a mine ends the game.
    """
    for x in range(easy_game.board.x_size):
        for y in range(easy_game.board.y_size):
            cell = easy_game.board.cells[x][y]
            if cell.is_mine:
                result = easy_game.reveal_cell(x, y)
                assert result == 'X'
                assert easy_game.game_over
                return  # Stop after finding the first mine

def test_game_win(easy_game):
    """
    Test winning the game by revealing all non-mined cells.
    """
    for x in range(easy_game.board.x_size):
        for y in range(easy_game.board.y_size):
            cell = easy_game.board.cells[x][y]
            if not cell.is_mine:
                result = easy_game.reveal_cell(x, y)
                assert result != 'X'
# Vérifie si la victoire est atteinte après avoir révélé toutes les cellules non minées
    easy_game.check_victory()
    assert easy_game.game_won