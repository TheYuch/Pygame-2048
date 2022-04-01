TILE_COLORS = {2: (200, 200, 200),
               4: (180, 180, 180),
               8: (160, 160, 160),
               16: (140, 140, 140),
               32: (120, 120, 120),
               64: (100, 100, 100),
               128: (80, 80, 80),
               256: (60, 60, 60),
               512: (40, 40, 40),
               1024: (20, 20, 20),
               2048: (0, 0, 0)}
NUM_COLORS = {2: (20, 20, 20),
              4: (40, 40, 40),
              8: (60, 60, 60),
              16: (80, 80, 80),
              32: (100, 100, 100),
              64: (120, 120, 120),
              128: (140, 140, 140),
              256: (160, 160, 160),
              512: (180, 180, 180),
              1024: (200, 200, 200),
              2048: (220, 220, 220)}
for i in range(10):
    TILE_COLORS.update({pow(2, i + 12): (0, 0, 0)})
    NUM_COLORS.update({pow(2, i + 12): (255, 255, 255)})
BLANK_TILE_COLOR = (200, 100, 0)
BG_COLOR = (255, 165, 0)

GAME_OVER_COLOR = (245, 230, 200)
GAME_OVER_FINISH_ALPHA = 200
GAME_OVER_BLIT_COUNT = 40
GAME_OVER_START_ALPHA = GAME_OVER_FINISH_ALPHA / GAME_OVER_BLIT_COUNT
GAME_OVER_FONT_SIZE = 50
GAME_OVER_TEXT = "Game over!"
GAME_OVER_TEXT_COLOR = (100, 100, 100)

WINDOW_SIZE = 512
WIDTH = WINDOW_SIZE
HEIGHT = WINDOW_SIZE
FPS = 60
TITLE = "2048"

GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE / GRID_SIZE
TILE_PADDING = TILE_SIZE / 16
TILE_DRAW_SIZE = TILE_SIZE - (TILE_PADDING * 2)
TILE_BORDER_RADIUS = int(TILE_PADDING)

TILE_MOVE_SPEED = 15
STOP_MOVE_DISTANCE = 4
TILE_GROW_SPEED = 10
STOP_GROW_WIDTH = 2
INDICATOR_SIZE_CHANGE = 1