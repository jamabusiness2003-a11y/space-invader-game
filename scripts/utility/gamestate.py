from settings.imports import *

# game state using enum
class GameState(Enum):
    MAIN_MENU = 1
    GAMEPLAY = 2
    PAUSE = 3
    GAME_OVER = 4
    SETTINGS = 5
