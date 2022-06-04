from collections import deque

import torch
import random

from model import Linear_QNet, QTrainer
from additional_functions import plot
from game_ai import SnakeGameAI

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(6, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    

    def get_action(self, state):
        # predict next action
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def remember(self, state, action, reward, new_state, game_over):
        self.memory.append((state, action, reward, new_state, game_over))

    def train_short_memory(self, state, action, reward, new_state, game_over):
        self.trainer.train_step(state, action, reward, new_state, game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)



def train(game_parameters=None):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    if game_parameters != None:
        game = SnakeGameAI(**game_parameters)
    else:
        gme = SnakeGameAI
    while True:
        # get current state of the game 
        old_state = game.get_state()

        # predict next move
        next_move = agent.get_action(old_state)

        # play the predicted next move
        game_over, reward, score = game.play(next_move, agent.n_games)

        # get new state of the game
        new_state = game.get_state()

        # train short memory
        agent.train_short_memory(old_state, next_move, reward, new_state, game_over)

        # remember
        agent.remember(old_state, next_move, reward, new_state, game_over)

        if game_over:
            # reset game
            game.reset()
            agent.n_games +=1

            # train long memory
            agent.train_long_memory()

            # update record
            if score > record:
                record = score
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot scores
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
    

if __name__ == '__main__':
    game_parameters= {'radars_range': 8}
    train(game_parameters)