import pygame

from minesweeper.views.vertical_layout import Widget

BASE_COLOR = (88, 101, 242)
HOVERED_COLOR = (138, 151, 242)
SELECTED_COLOR = (138, 180, 248)
WHITE_COLOR = (255, 255, 255)


class ButtonBase(Widget):
    PADDING = 5

    def __init__(self, label: str, width: int, height: int, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y, width=width, height=height)
        self.label = label
        self.is_hovered = False
        self.is_selected = False
        self.callback = None
        self.button_font = pygame.font.SysFont(None, 36)

    def connect(self, callback):
        """Connect a callback to the button"""
        self.callback = callback

    def handle_input(self, event):
        """Handle input for the button"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos) and self.callback:
                self.is_selected = True
                self.callback()


class BackButton(ButtonBase):
    def __init__(
        self, icon: pygame.Surface, width: int, height: int, x: int = 0, y: int = 0
    ):
        super().__init__("", width, height, x, y)

    def draw(self, screen: pygame.Surface):
        self.draw_background(screen)
        size = 20
        pygame.draw.polygon(
            self.screen,
            WHITE_COLOR,
            [
                (self.x, self.y),
                (self.x + size, self.y - size),
                (self.x + size, self.y + size),
            ],
        )

    def draw_background(self, screen):
        color = BASE_COLOR
        self.button_rect = pygame.Rect(
            self.x - self.PADDING, self.y - self.PADDING, self.width, self.height
        )
        if self.is_selected:
            color = SELECTED_COLOR
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            color = HOVERED_COLOR
        pygame.draw.rect(screen, color, self.button_rect, border_radius=10)


class Button(ButtonBase):
    def __init__(self, label: str, width: int, height: int, x: int = 0, y: int = 0):
        super().__init__(label, width, height, x, y)

    def draw_background(self, screen):
        color = BASE_COLOR

        self.button_rect = pygame.Rect(
            self.x - self.PADDING, self.y - self.PADDING, self.width, self.height
        )
        if self.is_selected:
            color = SELECTED_COLOR
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            color = HOVERED_COLOR

        pygame.draw.rect(screen, color, self.button_rect, border_radius=10)

    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen"""
        self.draw_background(screen)

        self.text_surface = self.button_font.render(self.label, True, WHITE_COLOR)

        x = self.x + (self.width - self.text_surface.get_width()) // 2
        y = self.y + (self.height - self.text_surface.get_height()) // 3
        screen.blit(
            self.text_surface,
            (
                x,
                y,
            ),
        )


class OptionButton(ButtonBase):
    def __init__(self, label: str, width: int, height: int, x: int = 0, y: int = 0):
        super().__init__(label, width, height, x, y)

    def draw_background(self, screen):
        color = BASE_COLOR

        self.button_rect = pygame.Rect(
            self.x - self.PADDING, self.y - self.PADDING, self.width, self.height
        )
        if self.is_selected:
            color = SELECTED_COLOR
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            color = HOVERED_COLOR

        radius = 8
        width = 0 if self.is_selected else 2
        pygame.draw.circle(
            screen,
            color,
            (self.x - self.PADDING, self.y + (self.height // 2) - (radius // 2)),
            width=width,
            radius=radius,
        )

    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen"""
        self.draw_background(screen)

        self.text_surface = self.button_font.render(self.label, True, WHITE_COLOR)

        x = self.x + self.PADDING * 2
        y = self.y + (self.height - self.text_surface.get_height()) // 3
        screen.blit(
            self.text_surface,
            (
                x,
                y,
            ),
        )
