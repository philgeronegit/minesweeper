from abc import ABC, abstractmethod

from minesweeper.models.board import EASY_DIFFICULTY


START_GAME_COMMAND = "start_game_command"
EASY_MODE_COMMAND = "easy_mode_command"
MEDIUM_MODE_COMMAND = "medium_mode_command"
HARD_MODE_COMMAND = "hard_mode_command"
REVEAL_CELL_COMMAND = "reveal_cell_command"
SET_FLAG_COMMAND = "set_flag_command"
SAVE_COMMAND = "save_command"
RESTORE_COMMAND = "restore_command"
SCORES_COMMAND = "scores_command"


class Command(ABC):
    """
    Abstract base class for Command objects.
    Concrete commands must implement the 'execute' method.
    """

    def __init__(self, receiver):
        """
        Initialize a command with a receiver.

        Args:
            receiver: The object that will perform the action when the command is executed.
        """
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        """
        Execute the command's action.
        """
        pass


class StartGameCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self):
        self.receiver.create_game()


class SaveCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self):
        self.receiver.save()


class RestoreCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self):
        self.receiver.restore()


class ScoresCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self):
        self.receiver.show_scores()


class SetDifficultyCommand(Command):
    def __init__(self, receiver, difficulty=EASY_DIFFICULTY):
        super().__init__(receiver)
        self.difficulty = difficulty

    def execute(self):
        self.receiver.set_difficulty(self.difficulty)


class RevealCellsCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self, x: int, y: int):
        self.receiver.reveal_cells(x, y)


class SetFlagCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self, x: int, y: int):
        self.receiver.set_flag(x, y)
