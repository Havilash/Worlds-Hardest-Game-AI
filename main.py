import gameObjects
import frames
import pygame
import pickle
import os
import neat
import sys

pygame.init()

WIN_SIZE = (1000, 800)
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("World Hardest Game")
FPS = 30

OBSTACLE_WIN = pygame.surface.Surface(WIN_SIZE)

GRID_SIZE = (25, 20)
GRID_SPACING = (WIN_SIZE[0]/GRID_SIZE[0], WIN_SIZE[1]/GRID_SIZE[1])
GRID_COLOR = "black"


def eval_genomes(genomes, config):
    is_running = True
    game_frame = frames.Game(genomes, config, WIN_SIZE, GRID_SIZE, GRID_SPACING)
    # level_creator_frame = frames.Level_Creator(WIN_SIZE, GRID_SIZE, GRID_SPACING)

    clock = pygame.time.Clock()
    while is_running and len(game_frame.players) > 0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                break

            game_frame.check_events(event)
            # level_creator_frame.check_events(event)
        
        game_frame.main(WIN, OBSTACLE_WIN)
        # level_creator_frame.main(WIN)



def level_creator():
    is_running = True
    level_creator_frame = frames.Level_Creator(WIN_SIZE, GRID_SIZE, GRID_SPACING)

    clock = pygame.time.Clock()
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                sys.exit()
                break                

            level_creator_frame.check_events(event)
        
        level_creator_frame.main(WIN)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 1000)
    pickle.dump(winner, open("winner.pickle", 'wb'))

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # level_creator()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
