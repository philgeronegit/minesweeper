import pygame

from minesweeper.controllers.command import (
    EASY_MODE_COMMAND,
    HARD_MODE_COMMAND,
    MEDIUM_MODE_COMMAND,
    SCORES_COMMAND,
    START_GAME_COMMAND,
    REVEAL_CELL_COMMAND,
    SET_FLAG_COMMAND,
    SAVE_COMMAND,
    RESTORE_COMMAND,
    RestoreCommand,
    SaveCommand,
    ScoresCommand,
    SetDifficultyCommand,
    StartGameCommand,
    RevealCellsCommand,
    SetFlagCommand,
)
from minesweeper.models.board import EASY_DIFFICULTY, MEDIUM_DIFFICULTY, HARD_DIFFICULTY
from minesweeper.models.game_state import GameState
from minesweeper.models.persistence import PicklePersistence
from minesweeper.views.game_view import GameView

# Constants
FPS = 60


class GameController:
    def __init__(self, model: GameState, view: GameView):
        self.model = model
        self.view = view
        self.clock = pygame.time.Clock()
        self.running = True
        self.create_commands()
        model.board.generate_mines()
        self.persistence = PicklePersistence()
        self.save_date = None

    def create_commands(self):
        """Create commands for the controller"""
        self.view.set_command(START_GAME_COMMAND, StartGameCommand(self))
        self.view.set_command(
            EASY_MODE_COMMAND, SetDifficultyCommand(self, EASY_DIFFICULTY)
        )
        self.view.set_command(
            MEDIUM_MODE_COMMAND, SetDifficultyCommand(self, MEDIUM_DIFFICULTY)
        )
        self.view.set_command(
            HARD_MODE_COMMAND, SetDifficultyCommand(self, HARD_DIFFICULTY)
        )
        self.view.set_command(REVEAL_CELL_COMMAND, RevealCellsCommand(self))
        self.view.set_command(SET_FLAG_COMMAND, SetFlagCommand(self))
        self.view.set_command(SAVE_COMMAND, SaveCommand(self))
        self.view.set_command(RESTORE_COMMAND, RestoreCommand(self))
        self.view.set_command(SCORES_COMMAND, ScoresCommand(self))

    def show_scores(self):
        self.view.show_scores_dialog()

    def create_game(self):
        """Create a new game"""
        print(f"Creating a new game with difficulty {self.model.board.difficulty} and grid size {self.model.board.x_size}x{self.model.board.y_size}")
        self.model.reset()
        self.view.reset(self.model.board.x_size, self.model.board.y_size)

    def set_difficulty(self, difficulty: str):
        """Set the difficulty of the game"""
        self.model.board.difficulty = difficulty

    def reveal_cells(self, x: int, y: int):
        """Reveal cells on the board"""
        try:
            self.model.board.reveal_cells(x, y)
        except ValueError:
            self.model.game_over = True

    def set_flag(self, x: int, y: int):
        """Set a flag on a cell"""
        self.model.board.set_flag(x, y)

    def restore(self):
        if self.persistence.is_file_exists():
            self.model = self.persistence.load()

    def save(self):
        self.persistence.dump(self.model)

    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.view.handle_input(event, self.model.game_over)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_input()
            self.view.draw(self.model)

            self.clock.tick(FPS)  # Cap the frame rate
