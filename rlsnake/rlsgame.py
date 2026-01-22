from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (38, 38, 38)
    RED = (200, 0, 0)
    GREEN = (29, 191, 72)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)

class Settings(Enum):
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    BLOCK_SIZE = 20
    SPEED = 15

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3