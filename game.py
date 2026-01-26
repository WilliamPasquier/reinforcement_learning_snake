import numpy as np
import pygame
from collections import namedtuple
from random import randint
from rlsnake import rlsgame

point = namedtuple('Point', 'x, y')
pygame.init()
font = pygame.font.Font(rlsgame.Settings.FONT_PATH.value, 14)

# Class definition
class SnakeRLGame:
    """
    Main game class handling the Snake game logic and environment.

    This class manages the game state, interactions, ui diplay and rules
    used for reinforcement learning.
    """
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
        '''
        Reset the score and draw first step snake and head
        '''
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

    def __place_food(self) -> None:
        '''
        Randomly places food on the game grid.

        If the food spawns on the snake, a new position is generated.

        '''
        x_coordonate = randint(0, (self.w - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        y_coordonate = randint(0, (self.h - rlsgame.Settings.BLOCK_SIZE.value) // rlsgame.Settings.BLOCK_SIZE.value) * rlsgame.Settings.BLOCK_SIZE.value
        self.food = point(x_coordonate, y_coordonate)
        if self.food in self.snake:
            self.__place_food()

    def play_step(self, action) -> tuple:
        '''
        Executes a single step of the game.
        - Get user inputs
        - Move the agent
        - Check if there is a collision
        - Check if food is eaten
        - Update the ui

        :return: A tuple containing:
            - whether the game is over,
            - the reward obtained for this step,
            - the current game score.
        :rtype: tuple
        '''
        reward = 0
        game_over = False
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Get key pressed and change direction according to keys
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w] and self.direction != rlsgame.Direction.DOWN.value:
        #     self.direction = rlsgame.Direction.UP.value

        # if keys[pygame.K_s] and self.direction != rlsgame.Direction.UP.value:
        #     self.direction = rlsgame.Direction.DOWN.value

        # if keys[pygame.K_a] and self.direction != rlsgame.Direction.RIGHT.value:
        #     self.direction = rlsgame.Direction.LEFT.value

        # if keys[pygame.K_d] and self.direction != rlsgame.Direction.LEFT.value:
        #     self.direction = rlsgame.Direction.RIGHT.value

        self.__move(action)
        
        # self.__hit_border()

        if self.__is_collision() or self.frame_iteration > self.__get_iteration_threshold():
            game_over = True
            reward -= 10  
            return game_over, reward, self.score

        if self.head == self.food:      #if the x and y coordonate of the tuple same -> food ate
            self.score += 1
            reward += 10
            self.__place_food()
        else:
            self.snake.pop()

        self.__update_ui()

        self.clock.tick(rlsgame.Settings.SPEED.value)

        return game_over, reward, self.score

    def __hit_border(self) -> None:
        '''
        Check if with hit the boundaries off the display and move the head to the opposite
        '''
        x_coordonate = self.head.x
        y_coordonate = self.head.y

        # Check if hit up border
        if self.head.y == -(rlsgame.Settings.BLOCK_SIZE.value):
            y_coordonate = self.h
            
        # Check if hit down border
        if self.head.y == self.h + rlsgame.Settings.BLOCK_SIZE.value:
            y_coordonate = -(rlsgame.Settings.BLOCK_SIZE.value)

        # Check if hit left border
        if self.head.x == -(rlsgame.Settings.BLOCK_SIZE.value):
            x_coordonate = self.w

        # Check if hit right border
        if self.head.x == self.w + rlsgame.Settings.BLOCK_SIZE.value:
            x_coordonate = -(rlsgame.Settings.BLOCK_SIZE.value)

        self.head = point(x_coordonate, y_coordonate)

    def __is_collision(self, pt=None) -> bool:
        '''
        Check if there is a collision between the head of the snake with the evironnement
        
        :param pt: Point with x and y coordonate
        :return: True value if there is a collision between the head and the environement
        :rtype: bool
        '''
        if pt is None:
            pt = self.head

        # Check if head hit the snake body
        if pt in self.snake[1:]:
            return True
        
        # Check if head hit the window border
        if pt.x > self.w - rlsgame.Settings.BLOCK_SIZE.value or pt.x < 0 or pt.y > self.h - rlsgame.Settings.BLOCK_SIZE.value or pt.y < 0:
            return True

        return False

    def __update_ui(self) -> None:
        '''
        Update UI
        The UI is composed of :
        - The background
        - The snake head and body
        - The food
        - All texts to get information on the current state
        '''
        current_state = self.get_state()

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

        self.__display_coordonate(self.head, "Snake head", [20, 20])
        self.__display_coordonate(self.food, "Food", [20, 40])
        self.__display_score([20, 60])
        self.__display_state(current_state, 80, 20)

        pygame.display.flip()

    def __display_coordonate(self, point, text, position) -> None:
        '''
        Display coordonate of a point on the window
        
        :param point: Point to display
        :param text: Text to display
        :param display_coordonate: List of x and y coordonate. Position of the text to display
        '''
        x_coordonate = point.x
        y_coordonate = point.y
        text = font.render(
            f"{text} (x, y) : {x_coordonate}, {y_coordonate}", 
            True, 
            rlsgame.Color.WHITE.value
        )
        self.display.blit(text, position)

    def __display_score(self, position) -> None:
        '''
        Docstring pour __display_score
        
        :param position: Position of the text to display
        '''
        text = font.render(
            f"Score : {self.score}, Iteration : {self.frame_iteration}/{self.__get_iteration_threshold()}",
            True,
            rlsgame.Color.WHITE.value
        )
        self.display.blit(text, position)

    def __display_state(self, state, start, gap) -> None:
        '''
        Display coordonate of a point on the window
        
        :param state: State array
        :param start: Start position
        :param gap: Gap between text
        '''
        danger_list = state[0:4]
        direction_list = state[4:8]
        direction_list = state[8:]

        # for index, danger in enumerate(rlsgame.Movement):
        #     state = danger_list[index]

        text = font.render(
            f"Step state : {state}", 
            True, 
            rlsgame.Color.WHITE.value
        )
        self.display.blit(text, [20, start])

    def __move(self, action) -> None:
        '''
        Move snake head according to the current direction
        
        :param action: Description
        '''
        self.direction = self.__change_direction(action)

        x_coordonate = self.head.x
        y_coordonate = self.head.y
        deplacement = rlsgame.Settings.BLOCK_SIZE.value

        if self.direction == rlsgame.Direction.UP.value:
            y_coordonate -= deplacement

        if self.direction == rlsgame.Direction.DOWN.value:
            y_coordonate += deplacement

        if self.direction == rlsgame.Direction.LEFT.value:
            x_coordonate -= deplacement

        if self.direction == rlsgame.Direction.RIGHT.value:
            x_coordonate += deplacement

        self.head = point(x_coordonate, y_coordonate)
        self.snake.insert(0,  self.head)

    def __change_direction(self, action) -> int:
        '''
        Docstring pour __change_direction
        
        :param action: Description
        '''
        clock_wise_movement = [direction.value for direction in rlsgame.Direction]
        index = clock_wise_movement[self.direction]
        if np.array_equal(action, [1, 0, 0]):               # straight / no change
            new_dir = clock_wise_movement[index]  
        elif np.array_equal(action, [0, 1, 0]):             # right turn / u -> r -> d -> l
            next_idx = (index + 1) % 4
            new_dir = clock_wise_movement[next_idx]  
        elif np.array_equal(action, [0, 0, 1]):             # left turn / u -> l -> d -> r
            next_idx = (index - 1) % 4
            new_dir = clock_wise_movement[next_idx]  

        return new_dir

    def get_state(self) -> np.ndarray:
        '''
        Returns the current state of the game for the agent.

        The state is represented as a binary vector describing:
        - potential dangers (straight, right, left),
        - current movement direction,
        - relative position of the food compared to the snake's head.

        :return: A NumPy array of integers representing the game state.
        '''
        state = [
            self.__check_danger(rlsgame.Movement.STRAIGHT),
            self.__check_danger(rlsgame.Movement.RIGHT),
            self.__check_danger(rlsgame.Movement.LEFT),
            self.__check_direction(rlsgame.Direction.UP),
            self.__check_direction(rlsgame.Direction.RIGHT),
            self.__check_direction(rlsgame.Direction.DOWN),
            self.__check_direction(rlsgame.Direction.LEFT),
            self.food.x < self.head.x,
            self.food.x > self.head.x,
            self.food.y < self.head.y,
            self.food.y > self.head.y
        ]

        return np.array(state, dtype=int)

    def __get_sensor_point(self) -> dict:
        '''
        Get sensor point of the snake head
        
        :return: Sensor point dictionnary
        :rtype: dict
        '''
        block = rlsgame.Settings.BLOCK_SIZE.value
        x = self.head.x
        y = self.head.y

        directions = {
            rlsgame.Direction.UP.name: (0, -block),
            rlsgame.Direction.RIGHT.name: (block, 0),
            rlsgame.Direction.DOWN.name: (0, block),
            rlsgame.Direction.LEFT.name: (-block, 0),
        }

        return {
            direction: point(x + dx, y + dy)
            for direction, (dx, dy) in directions.items()
        }

    def __check_danger(self, movement:rlsgame.Movement) -> bool:
        '''
        Check if there is a danger in the agent movement
        
        :param movement: Movement in the point of view of the agent
        :type movement: rlsgame.Mouvement
        :return: Description
        :rtype: True if there is a danger in the agent movement
        '''
        pattern = rlsgame.DANGER_PATTERN[movement.value]
        sensor = self.__get_sensor_point()

        for direction in rlsgame.Direction:
            is_direction = self.__check_direction(direction)
            is_collision = self.__is_collision(sensor[pattern[direction.value].name])
            if is_direction and is_collision:
                return True

        return False
    
    def __check_direction(self, direction:rlsgame.Direction) -> bool:
        '''
        Check the current direction
        
        :param direction: Direction do check
        :type direction: rlsgame.Direction
        :return: True if the current correspond
        :rtype: bool
        '''
        return self.direction == direction.value
    
    def __get_iteration_threshold(self) -> int:
        return 100*len(self.snake)
