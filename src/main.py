import pygame

pygame.init()

from game_app import GameApp  # noqa: E402


def main():
    app = GameApp()
    app.run()


if __name__ == "__main__":
    main()
