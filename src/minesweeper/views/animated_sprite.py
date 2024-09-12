import pygame

EXPLOSION_IMG = "src/minesweeper/assets/explosion.png"
TRANSPARENT_COLOR = (27, 26, 29)
explosion_sheet = pygame.image.load(EXPLOSION_IMG)
explosion_sheet.set_colorkey(TRANSPARENT_COLOR)

NUMBER_OF_FRAMES = 7
FPS = 3

NUM_COLUMNS = 4
NUM_ROWS = 2
TOTAL_FRAMES = NUM_COLUMNS * NUM_ROWS  # Total number of frames (2x4 = 8)
RESIZED_FRAME_WIDTH = 48
RESIZED_FRAME_HEIGHT = 48

FRAME_WIDTH = (
    explosion_sheet.get_width() // NUM_COLUMNS
)  # Calculate width of each frame
FRAME_HEIGHT = explosion_sheet.get_height() // NUM_ROWS


frames = []
for row in range(NUM_ROWS):
    for col in range(NUM_COLUMNS):
        frame = explosion_sheet.subsurface(
            pygame.Rect(
                col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT
            )
        )
        resized_frame = pygame.transform.scale(
            frame, (RESIZED_FRAME_WIDTH, RESIZED_FRAME_HEIGHT)
        )
        frames.append(resized_frame)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()
        self.animation_complete = False

    def update(self):
        """Update the sprite animation. Stop after all frames are shown."""
        if not self.animation_complete:
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 // FPS:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.animation_complete = (
                        True  # Set the flag when animation is done
                    )
                else:
                    self.image = self.frames[self.current_frame]

    def has_finished(self):
        """Return whether the animation has finished."""
        return self.animation_complete
