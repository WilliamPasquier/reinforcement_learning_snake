import numpy as np
import pygame
from collections import namedtuple
from random import randint
from rlsnake import rlsgame

point = namedtuple('Point', 'x, y')
pygame.init()

# Class definition
class SnakeRLGame:
    def __init__(
            self, 
            w=rlsgame.Settings.WINDOW_WIDTH.value,
            h=rlsgame.Settings.WINDOW_HEIGHT.value
        ):
        # Declare properties
        self.w = w
        self.h = h
        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self.direction = 0
        
        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Reinforcement Learning Snake")

        # Init pygame ticking
        self.clock = pygame.time.Clock()

        # Set base value
        self.reset()
       
    def reset(self):
        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self.direction = 0
        
        self.head = point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            point(self.head.x - rlsgame.Settings.BLOCK_SIZE.value, self.head.y),
            point(self.head.x - (2 * rlsgame.Settings.BLOCK_SIZE.value), self.head.y)
        ]

        self.__place_food()


    def __place_food(self):
        x_coordonate = randint(0, (self.w - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        y_coordonate = randint(0, (self.h - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        self.food = point(x_coordonate, y_coordonate)
        if self.food in self.snake:
            self.__place_food()

    def play_step(self):
        reward = 0
        game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != rlsgame.Direction.DOWN.value:
            self.direction = rlsgame.Direction.UP.value

        if keys[pygame.K_s] and self.direction != rlsgame.Direction.UP.value:
            self.direction = rlsgame.Direction.DOWN.value

        if keys[pygame.K_a] and self.direction != rlsgame.Direction.RIGHT.value:
            self.direction = rlsgame.Direction.LEFT.value

        if keys[pygame.K_d] and self.direction != rlsgame.Direction.LEFT.value:
            self.direction = rlsgame.Direction.RIGHT.value

        self.__move()

        self.__hit_border()

        if self.head == self.food:      #if the x and y coordonate of the tuple same -> food ate
            self.score += 1
            reward += 10
            self.__place_food()
            print(f"Food ate, score : {self.score}")
        else:
            self.snake.pop()

        if self.is_collision():
            game_over = True
            reward -= 10  
            return game_over, reward, self.score

        self.__update_ui()
        self.clock.tick(rlsgame.Settings.SPEED.value)

        return game_over, reward, self.score

    def __hit_border(self):
        x_coordonate = self.head.x
        y_coordonate = self.head.y

        # Check if hit up border
        if self.head.y <= -(rlsgame.Settings.BLOCK_SIZE.value):
            y_coordonate = self.h
            
        # Check if hit down border
        if self.head.y >= self.h + rlsgame.Settings.BLOCK_SIZE.value:
            y_coordonate = -(rlsgame.Settings.BLOCK_SIZE.value)

        # Check if hit left border
        if self.head.x <= -(rlsgame.Settings.BLOCK_SIZE.value):
            x_coordonate = self.w

        # Check if hit right border
        if self.head.x >= self.w + rlsgame.Settings.BLOCK_SIZE.value:
            x_coordonate = -(rlsgame.Settings.BLOCK_SIZE.value)

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
        
    def __move(self) -> None:
        x_coordonate = self.head.x
        y_coordonate = self.head.y

        if self.direction == rlsgame.Direction.UP.value:
            y_coordonate -= rlsgame.Settings.BLOCK_SIZE.value

        if self.direction == rlsgame.Direction.DOWN.value:
            y_coordonate += rlsgame.Settings.BLOCK_SIZE.value

        if self.direction == rlsgame.Direction.LEFT.value:
            x_coordonate -= rlsgame.Settings.BLOCK_SIZE.value

        if self.direction == rlsgame.Direction.RIGHT.value:
            x_coordonate += rlsgame.Settings.BLOCK_SIZE.value

        self.head = point(x_coordonate, y_coordonate)
        self.snake.insert(0,  self.head)
