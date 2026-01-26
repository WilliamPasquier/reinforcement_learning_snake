import random
import torch
from collections import deque
from model import Linear_QNet, QTrainer
from rlsnake import rlsmodel

class Agent:
    '''
    Docstring pour Agent
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

    def remember(self, previous_state, action, reward, new_state, is_done) -> None:
        self.memory.append((previous_state, action, reward, new_state, is_done))
    
    def train_long_memory(self) -> None:
        if len(self.memory) > rlsmodel.Memory.BATCH_SIZE.value:
            mini_sample = random.sample(self.memory, rlsmodel.Memory.BATCH_SIZE.value)
        else:
            mini_sample = self.memory

        previous_states, actions, rewards, new_states, is_dones = zip(*mini_sample)
        self.trainer.train_step(previous_states, actions, rewards, new_states, is_dones)
        
    def train_short_memory(self, previous_state, action, reward, new_state, is_done) -> None:
        self.trainer.train_step(previous_state, action, reward, new_state, is_done)

    def get_action(self, state) -> list:
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move