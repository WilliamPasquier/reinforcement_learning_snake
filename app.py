import sys
from agent import Agent
from game import SnakeRLGame
from helper import plot
from rlsnake import rlshelper

def train(game: SnakeRLGame, agent:Agent) -> None:
    '''
    Docstring pour train
    
    :param game: Game instance
    :type game: SnakeRLGame
    :param agent: Agent instance
    :type agent: Agent
    '''
    record = 0

    # Plot list
    plot_scores = []
    plot_mean_scores = []
    total_score = 0

    while True:
        previous_state = game.get_state()
        final_move = agent.get_action(previous_state)
        is_done, reward, score = game.play_step(final_move)
        new_state = game.get_state()
        agent.train_short_memory(previous_state, final_move, reward, new_state, is_done)
        agent.remember(previous_state, final_move, reward, new_state, is_done)

        if is_done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # Save model
            if rlshelper.Settings.SAVE_MODEL.value and score > record:
                agent.save_model(score)
                record = score

            # Plot score and mean score
            if rlshelper.Settings.PLOT.value:
                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    print("Reinforcement Learning Snake agent")

    # Create instances
    environnement = SnakeRLGame()
    agent = Agent()

    if len(sys.argv) > 1:
        model_path = sys.argv[1]
        agent.load_model(model_path)
        
    train(environnement, agent)