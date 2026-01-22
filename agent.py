from game import SnakeRLGame

# Constante definition

class Agent:
    def __init__(self):
        pass

    def get_state(self, game):
        pass

    def remember(self):
        pass
    
    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action():
        pass

    
def train():
    game = SnakeRLGame()

    while True:
        is_done, reward, score = game.play_step()

        if is_done:
            game.reset()


if __name__ == '__main__':
    print("Reinforcement Learning Snake agent")
    train()