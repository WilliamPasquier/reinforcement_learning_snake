import os
import random
import torch
from collections import deque
from datetime import datetime
from model import Linear_QNet, QTrainer
from rlsnake import rlsmodel, rlshelper

class Agent:
    '''
    Agent class containing the model and the training logic.
    '''
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=rlsmodel.Memory.MAX_MEMORY.value)
        self.model = Linear_QNet(
            rlsmodel.Network.INPUT.value,
            rlsmodel.Network.HIDDEN.value,
            rlsmodel.Network.OUTPUT.value
        )
        self.trainer = QTrainer(self.model, rlsmodel.Memory.LEARNING_RATE.value, self.gamma)
        self.is_model_load = False

    def remember(self, previous_state, action, reward, new_state, is_done) -> None:
        '''
        Remember action and states differences
        
        :param previous_state: State before movement
        :param action: Action performed by the agent
        :param reward: How well the action was
        :param new_state: New state after movement
        :param is_done: If the game is over (collsion / out of iteration)
        '''
        self.memory.append((previous_state, action, reward, new_state, is_done))
    
    def train_long_memory(self) -> None:
        '''
        Train model long memory
        '''
        if len(self.memory) > rlsmodel.Memory.BATCH_SIZE.value:
            mini_sample = random.sample(self.memory, rlsmodel.Memory.BATCH_SIZE.value)
        else:
            mini_sample = self.memory

        previous_states, actions, rewards, new_states, is_dones = zip(*mini_sample)
        self.trainer.train_step(previous_states, actions, rewards, new_states, is_dones)
        
    def train_short_memory(self, previous_state, action, reward, new_state, is_done) -> None:
        '''
        Train model short memory
        
        :param previous_state: Game state before movement
        :param action: Action performed by the agent
        :param reward: How well the action was
        :param new_state: New game state after movement
        :param is_done: If the game is over (collsion / out of iteration)
        '''
        self.trainer.train_step(previous_state, action, reward, new_state, is_done)

    def get_action(self, state) -> list:
        '''
        Get action the agent will performed based on randomness or not
        
        :param state: Game sate
        :return: List of possible action
        :rtype: list
        '''
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon and self.is_model_load == False:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
    def save_model(self, score) -> None:
        '''
        Save model
        '''
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        hour_str = now.strftime("%H-%M-%S")

        model_path = os.path.join(rlshelper.Settings.MODEL_PATH.value, date_str)
        file_name = f'model_{hour_str}_score-{score}_epoch-{self.n_games}.pth'

        self.model.save_model(model_path, file_name)

    def load_model(self, model_path) -> None:
        '''
        Load model
        '''
        if not os.path.isfile(model_path):
            return
        
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.eval()
        self.is_model_load = True
