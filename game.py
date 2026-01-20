import numpy as np
import pygame
from collections import namedtuple
from random import randint
from rlsnake import rlsgame

point = namedtuple('Point', 'x, y')
pygame.init()

# Class definition
class SnakeRLGame:
    def __init__(self, w=rlsgame.Settings.WINDOW_WIDTH.value, h=rlsgame.Settings.WINDOW_HEIGHT.value):
       self.w = w
       self.h = h

       # Init display
       self.display = pygame.display.set_mode((self.w, self.h))
       pygame.display.set_caption("Reinforcement Learning Snake")

       # Init pygame ticking
       self.clock = pygame.time.Clock()
       self.reset()
       
    def reset(self):
        self.head = point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            point(self.head.x - rlsgame.Settings.BLOCK_SIZE.value, self.head.y),
            point(self.head.x - (2 * rlsgame.Settings.BLOCK_SIZE.value), self.head.y)
        ]

        self.score = 0
        self.food = None
        self.__place_food()
        self.frame_iteration = 0

    def __place_food(self):
        x_coordonate = randint(0, (self.w - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        y_coordonate = randint(0, (self.w - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        self.food = point(x_coordonate, y_coordonate)
        if self.food in self.snake:
            self.__place_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.__move()

        self.__hit_border()

        if self.head == self.food:
            self.score += 10
            self.__place_food()
            print(f"Food ate, score : {self.score}")
        else:
            self.snake.pop()

        self.__update_ui()
        self.clock.tick(rlsgame.Settings.SPEED.value)

    def __hit_border(self):
        x_coordonate = self.head.x
        y_coordonate = self.head.y

        # Check if hit up border
        if self.head.y == -(rlsgame.Settings.BLOCK_SIZE.value):
            y_coordonate = self.h
            
        # Check if hit down border
        if self.head.y == self.h + rlsgame.Settings.BLOCK_SIZE.value:
            y_coordonate = 0

        # Check if hit left border
        if self.head.x == -(rlsgame.Settings.BLOCK_SIZE.value):
            x_coordonate = self.w

        # Check if hit right border
        if self.head.x == self.w + rlsgame.Settings.BLOCK_SIZE.value:
            x_coordonate = 0

        self.head = point(x_coordonate, y_coordonate)

    def is_collision(self, pt=None) -> bool:
        '''
        Check if there is a collision between the head of the snake with the evironnement
        
        :param self: Description
        :param pt: Point with x and y coordonate
        :return: True value if there is a collision between the head and the environement
        :rtype: bool
        '''
        if pt is None:
            pt = self.head

        # Check if head hit the snake body
        if pt in self.snake[1:]:
            return True

        return False

    def __update_ui(self) -> None:
        '''
        Update UI by drawing the background, the snake and the food

        :param self: Description
        '''
        self.display.fill(rlsgame.Color.GREEN.value)

        # Draw snake body
        for pt in self.snake:
            pygame.draw.rect(
                self.display, 
                rlsgame.Color.BLUE1.value, 
                pygame.Rect(
                    pt.x,
                    pt.y,
                    rlsgame.Settings.BLOCK_SIZE.value,
                    rlsgame.Settings.BLOCK_SIZE.value
                )
            )

        # Draw food
        pygame.draw.rect(
            self.display,
            rlsgame.Color.RED.value,
            pygame.Rect(
                self.food.x,
                self.food.y,
                rlsgame.Settings.BLOCK_SIZE.value,
                rlsgame.Settings.BLOCK_SIZE.value
            )
        )

        pygame.display.flip()
        
    def __move(self):
        x_coordonate = self.head.x
        y_coordonate = self.head.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            y_coordonate -= rlsgame.Settings.BLOCK_SIZE.value
        if keys[pygame.K_s]:
            y_coordonate += rlsgame.Settings.BLOCK_SIZE.value
        if keys[pygame.K_a]:
            x_coordonate -= rlsgame.Settings.BLOCK_SIZE.value
        if keys[pygame.K_d]:
            x_coordonate += rlsgame.Settings.BLOCK_SIZE.value

        self.head = point(x_coordonate, y_coordonate)
        self.snake.insert(0,  self.head)

