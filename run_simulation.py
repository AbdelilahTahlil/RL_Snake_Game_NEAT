import os 

import neat

from game_ai import SnakeGameAI, Snake


def run_simulation(genomes, config):
    nets = []
    snakes = []


    # game settings 
    width= 640
    height= 480
    radars_range = 8
    snake_starting_x, snake_starting_y = width//2, height//2

    
    

    for genome_id, genome in genomes:
        
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake(snake_starting_x, snake_starting_y, radars_range, width, height))
    
    
    game = SnakeGameAI(nets, snakes)

    while True:
        game_over, rewards = game.play()
        
        i=0
        for genome_id, genome in genomes :
            genome.fitness += rewards[i]
            i+=1

        if game_over:
            break




if __name__ == '__main__' :
    config_path = os.path.join('neat', 'config.txt')
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
