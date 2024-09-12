import pygame

from minesweeper.controllers.command import (
    SCORES_COMMAND,
    START_GAME_COMMAND,
    EASY_MODE_COMMAND,
    MEDIUM_MODE_COMMAND,
    HARD_MODE_COMMAND,
    REVEAL_CELL_COMMAND,
    SET_FLAG_COMMAND,
    SAVE_COMMAND,
    RESTORE_COMMAND,
    START_TIME_COMMAND,
    Command,
)
from minesweeper.models.board import (
    DIFFICULTY_LEVELS,
    EASY_DIFFICULTY,
    MEDIUM_DIFFICULTY,
    HARD_DIFFICULTY,
)
from minesweeper.models.game_state import GameStateDTO
from minesweeper.models.cell import Cell
from minesweeper.views.animated_sprite import AnimatedExplosion
from minesweeper.views.button import Button, OptionButton
from minesweeper.views.vertical_layout import VerticalLayout

# Constants
DEBUG_MODE = True

GRID_SIZE = 9
CELL_SIZE = 40
MARGIN = 5
MENU_WIDTH = 200
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE + MARGIN * (GRID_SIZE + 1) + MENU_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE + MARGIN * (GRID_SIZE + 1)

NOT_REVEALED_IMG = pygame.image.load("src/minesweeper/assets/not_revealed.png")
BOMB_IMG = pygame.image.load("src/minesweeper/assets/bomb.png")
EMPTY_IMG = pygame.image.load("src/minesweeper/assets/empty.png")
FLAG_IMG = pygame.image.load("src/minesweeper/assets/flags.png")

LEFT_MARGIN = 20
BUTTON_WIDTH = 170
BUTTON_HEIGHT = 40

# Colors
LIGHT_RED = (255, 182, 193)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont(None, 24)
menu_font = pygame.font.SysFont(None, 36)


class GameView:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window_height = WINDOW_HEIGHT
        self.window_width = WINDOW_WIDTH
        self.menu_buttons = {}
        self.commands = {}
        self.show_scores = False
        pygame.display.set_caption("Minesweeper")
        self.all_sprites = None
        self.create_menu()

    @property
    def center(self):
        """Return the center of the window"""
        return (self.window_width // 2, self.window_height // 2)

    def handle_input(self, event, data: GameStateDTO):
        """Handle user input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < MENU_WIDTH:
                for button in self.menu_buttons.values():
                    button.handle_input(event)
            else:
                if data.game_over:
                    return
                grid_x = y // (CELL_SIZE + MARGIN)
                grid_y = (x - MENU_WIDTH) // (CELL_SIZE + MARGIN)
                print(f"Clicked on {grid_x}, {grid_y} and mouse button {event.button}")
                if event.button == 1:
                    self.commands[REVEAL_CELL_COMMAND].execute(grid_x, grid_y)
                    if not data.first_cell_revealed:
                        self.commands[START_TIME_COMMAND].execute()
                elif event.button == 3:
                    self.commands[SET_FLAG_COMMAND].execute(grid_x, grid_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_scores = False

    def set_command(self, action: str, command: Command):
        """Set a command for an action"""
        self.commands[action] = command

    def reset(self, grid_x_size: int, grid_y_size: int):
        """Reset the view"""
        self.window_width = (
            CELL_SIZE * grid_y_size + MARGIN * (grid_y_size + 1) + MENU_WIDTH
        )
        self.window_height = CELL_SIZE * grid_x_size + MARGIN * (grid_x_size + 1)
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        # center window on the screen after the grid has increased or decreased
        screen_rect = screen.get_rect()
        screen_rect.center = pygame.display.get_surface().get_rect().center
        pygame.display.get_surface().blit(screen, screen_rect)
        self.all_sprites = None

    def compute_rect(self, x: int, y: int):
        """Compute the rectangle for a cell"""
        return pygame.Rect(
            y * (CELL_SIZE + MARGIN) + MENU_WIDTH,
            x * (CELL_SIZE + MARGIN),
            CELL_SIZE,
            CELL_SIZE)

    def draw_cell(self, x: int, y: int, cell: Cell, data: GameStateDTO):
        """Draw a cell"""
        rect = self.compute_rect(x, y)
        if (data.game_over and cell.is_mine) or (DEBUG_MODE and cell.is_mine):
            self.screen.blit(BOMB_IMG, rect)
        elif cell.is_flagged:
            self.screen.blit(FLAG_IMG, rect)
        elif not cell.is_opened:
            self.screen.blit(NOT_REVEALED_IMG, rect)
        elif cell.adjacent_mines > 0:
            self.screen.blit(EMPTY_IMG, rect)
            text = font.render(str(cell.adjacent_mines), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(EMPTY_IMG, rect)

    def draw_board(self, data: GameStateDTO):
        """Draw the board"""
        cells = data.cells
        for x in range(len(cells)):
            for y in range(len(cells[0])):
                cell = cells[x][y]
                self.draw_cell(x, y, cell, data)
        if data.game_over:
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)                

    def __add_menu_buttons(self, btn, command_name: str):
        """Add menu button and connect it to a command"""
        self.menu_buttons[btn.label] = btn
        btn.connect(lambda: self.commands[command_name].execute())

    def create_menu(self):
        """Create the menu"""
        vertical_layout = VerticalLayout(left_margin=LEFT_MARGIN)
        new_game_btn = Button("New Game", BUTTON_WIDTH, BUTTON_HEIGHT)
        easy_mode_btn = OptionButton(
            EASY_DIFFICULTY.capitalize(), BUTTON_WIDTH, BUTTON_HEIGHT
        )
        easy_mode_btn.is_selected = True
        medium_mode_btn = OptionButton(
            MEDIUM_DIFFICULTY.capitalize(), BUTTON_WIDTH, BUTTON_HEIGHT
        )
        hard_mode_btn = OptionButton(
            HARD_DIFFICULTY.capitalize(), BUTTON_WIDTH, BUTTON_HEIGHT
        )
        save_btn = Button("Save", BUTTON_WIDTH, BUTTON_HEIGHT)
        restore_btn = Button("Restore", BUTTON_WIDTH, BUTTON_HEIGHT)
        scores_btn = Button("Scores", BUTTON_WIDTH, BUTTON_HEIGHT)
        vertical_layout.add(new_game_btn)
        vertical_layout.add(easy_mode_btn)
        vertical_layout.add(medium_mode_btn)
        vertical_layout.add(hard_mode_btn)
        vertical_layout.add(save_btn)
        vertical_layout.add(restore_btn)
        vertical_layout.add(scores_btn)

        self.__add_menu_buttons(new_game_btn, START_GAME_COMMAND)
        self.__add_menu_buttons(easy_mode_btn, EASY_MODE_COMMAND)
        self.__add_menu_buttons(medium_mode_btn, MEDIUM_MODE_COMMAND)
        self.__add_menu_buttons(hard_mode_btn, HARD_MODE_COMMAND)
        self.__add_menu_buttons(save_btn, SAVE_COMMAND)
        self.__add_menu_buttons(restore_btn, RESTORE_COMMAND)
        self.__add_menu_buttons(scores_btn, SCORES_COMMAND)

    def draw_menu(self, data: GameStateDTO):
        """Draw the menu"""
        pygame.draw.rect(
            self.screen, (200, 200, 200), (0, 0, MENU_WIDTH, self.window_height)
        )

        for key, button in self.menu_buttons.items():
            if key.lower() in DIFFICULTY_LEVELS.keys():
                button.is_selected = False
        self.menu_buttons[data.difficulty.capitalize()].is_selected = True

        for button in self.menu_buttons.values():
            button.draw(self.screen)

        STATS_Y = 320
        if not data.game_over and not data.game_won:
            timer_text = menu_font.render(f"Time: {data.ellapsed_time}", True, BLACK)
            self.screen.blit(timer_text, (LEFT_MARGIN, STATS_Y))

            mines_left = data.get_remaining_mines()
            mines_text = menu_font.render(f"Mines: {mines_left}", True, BLACK)
            self.screen.blit(mines_text, (LEFT_MARGIN, STATS_Y + 40))
        if data.game_won:
            time_text = menu_font.render(f"Won in : {data.won_time}", True, BLACK)
            self.screen.blit(time_text, (LEFT_MARGIN, STATS_Y))

    def draw_status(self, data: GameStateDTO):
        """Draw status: check if the game is won or over"""
        if data.game_over:
            self.__draw_message("Game over", LIGHT_RED)
        elif data.check_victory():
            self.__draw_message("You Win!", LIGHT_BLUE)

    def __draw_message(self, text: str, background_color: str):
        """Draw a message on the screen"""
        font = pygame.font.SysFont(None, 72)

        text = font.render(text, True, BLACK)

        text_rect = text.get_rect(center=self.center)

        PADDING = 20
        background_rect = pygame.Surface(
            (text_rect.width + PADDING, text_rect.height + PADDING)
        )
        background_rect.fill(background_color)

        background_rect_rect = background_rect.get_rect(center=self.center)

        self.screen.blit(background_rect, background_rect_rect)
        self.screen.blit(text, text_rect)

    def show_scores_dialog(self):
        """Show the best scores dialog"""
        self.show_scores = True

    def draw_best_scores(self, data: GameStateDTO):
        """Show the best scores"""
        if not self.show_scores:
            return

        # create a dialog box like surface with a title, a list of the two best scores and a close button
        dialog_width = 400
        dialog_height = 300
        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill((255, 255, 255))
        dialog_rect = dialog_surface.get_rect(center=self.center)
        self.screen.blit(dialog_surface, dialog_rect)
        # draw the title
        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("Best Scores", True, BLACK)
        title_rect = title_text.get_rect(center=(self.center[0], dialog_rect.top + 30))
        self.screen.blit(title_text, title_rect)

        # draw the best scores
        scores = data.best_scores
        scores_font = pygame.font.SysFont(None, 24)
        y = title_rect.bottom + 20
        for score in scores:
            score_text = scores_font.render(score, True, BLACK)
            score_rect = score_text.get_rect(center=(self.center[0], y))
            self.screen.blit(score_text, score_rect)
            y += 30

    def draw(self, model: GameStateDTO):
        """Draw the game"""
        if self.all_sprites is None:
            self.all_sprites = pygame.sprite.Group()
            for mine in model.mines:
                print(f"Creating explosion at {mine.x} {mine.y}")
                rect = self.compute_rect(mine.x, mine.y)
                explosion = AnimatedExplosion(rect.centerx, rect.centery)      
                self.all_sprites.add(explosion)
        self.draw_menu(model)
        self.draw_board(model)
        self.draw_status(model)
        self.draw_best_scores(model)
        pygame.display.flip()
