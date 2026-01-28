from enum import Enum

class Settings(Enum):
    '''
    Pygame settings
    '''
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 640
    BLOCK_SIZE = 20
    SPEED = 80
    FONT_PATH = './font/arial.ttf'

class Direction(Enum):
    '''
    Possible direction in-game
    '''
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Movement(Enum):
    '''
    Possible movement of the agent
    '''
    STRAIGHT = 'Straight'
    RIGHT = 'Right'
    LEFT = 'Left'

# Different danger pattern mapped with the direction value
# Exemple : Direction.UP.value -> index of direction to check for each movement
DANGER_PATTERN = {
    Movement.STRAIGHT.value: [
        Direction.UP,
        Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT
    ],
    Movement.RIGHT.value: [
        Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT,
        Direction.UP
    ],
    Movement.LEFT.value: [
        Direction.LEFT,
        Direction.UP,
        Direction.RIGHT,
        Direction.DOWN
    ],
}

class Color(Enum):
    '''
    Colors
    '''
    WHITE = (255, 255, 255)
    BLACK = (38, 38, 38)
    RED = (200, 0, 0)
    GREEN = (29, 191, 72)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    ORANGE = (232, 103, 31)
    ORANGE2 = (229, 146, 83)
