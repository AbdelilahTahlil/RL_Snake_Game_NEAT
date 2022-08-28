"""
Execute this file to run the game.
"""

import os
import math

import neat

from functions.game_ai import SnakeGameAI, Snake
from functions.visualize import plot_stats, plot_species


def run_simulation(genomes, config): #pylint: disable=redefined-outer-name
    nets = []
    snakes = []


    # game settings
    width= 640
    height= 480
    radars_range = 10
    snake_starting_x, snake_starting_y = width//2, height//2


    for genome_id, genome in genomes: #pylint: disable=unused-variable

        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake(snake_starting_x, snake_starting_y, radars_range, width, height))


    game = SnakeGameAI(nets, snakes)

    while True:
        game_over, still_alive, rewards = game.play() #pylint: disable=unused-variable
        #print('Still alive:', still_alive)
        #print('Number of snakes:', len(game.snakes))

        i=0
        for genome_id, genome in genomes :
            genome.fitness += rewards[i]
            i+=1

        if game_over:
            break

def tanh(z):
    z = max(-60.0, min(60.0, 2.5 * z))
    return math.tanh(z)

def relu(z):
    return z if z > 0.0 else 0.0

def elu(z):
    return z if z > 0.0 else math.exp(z) - 1

def identity(z):
    return z

if __name__ == '__main__' :
    config_path = os.path.join('config/config.txt')
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    config.genome_config.add_activation('tanh', tanh)
    config.genome_config.add_activation('relu', relu)
    config.genome_config.add_activation('elu', elu)
    config.genome_config.add_activation('identity', identity)
    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of 1000 Generations
    winner = population.run(run_simulation, 1000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner)) #pylint: disable=consider-using-f-string

    plot_stats(stats, ylog=False, view=True)
    plot_species(stats, view=True)
