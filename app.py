from game import SnakeRLGame
from agent import Agent

def train() -> None:
    '''
    Train the agent
    '''
    game = SnakeRLGame()
    agent = Agent()
    record = 0

    while True:
        previous_state = game.get_state()
        final_move = agent.get_action(previous_state)
        is_done, reward, score = game.play_step(final_move)
        # is_done, reward, score = game.play_step(None)
        new_state = game.get_state()
        agent.train_short_memory(previous_state, final_move, reward, new_state, is_done)
        agent.remember(previous_state, final_move, reward, new_state, is_done)

        if is_done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            record = max(record, score)
            print('Game', agent.n_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    print("Reinforcement Learning Snake agent")
    train()