# main.py
import neat
import pygame
import os
from flappy_bird import Bird

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        bird = Bird(230, 350)

        run = True
        while run:
            bird.move()
            output = net.activate((bird.y, 0, 0))  # Input = bird.y, pipe.top, pipe.bottom

            if output[0] > 0.5:
                bird.jump()

            # Simulate pipe, base, scoring etc. here
            genome.fitness += 1  # Reward for staying alive

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run(config_path)
