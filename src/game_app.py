from minesweeper.controllers.game_controller import GameController
from minesweeper.models.game_state import GameState
from minesweeper.views.game_view import GameView


class GameApp:
    def __init__(self):
        model = GameState()
        view = GameView()
        self.controller = GameController(model, view)

    def run(self):
        self.controller.run()


if __name__ == "__main__":
    game = GameApp()
    game.run()
