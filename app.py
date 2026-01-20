import pygame
from collections import namedtuple

# Constante definition
# Window size
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Color palette (RGB)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREEN = (29, 191, 72)
BLACK = (38, 38, 38)

# Block setting
BLOCK_SIZE = 20

# Game speed
SPEED = 100

if __name__ == "__main__":
    point = namedtuple('Point', 'x, y')

    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREEN)

        pygame.display.flip()
        
        head = point(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        clock.tick(60)

    pygame.quit()