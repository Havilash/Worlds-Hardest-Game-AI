import gameObjects
import frames
import pygame
import pickle

pygame.init()

WIN_SIZE = (1000, 800)
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("World Hardest Game")
FPS = 60

GRID_SIZE = (25, 20)
GRID_SPACING = (WIN_SIZE[0]/GRID_SIZE[0], WIN_SIZE[1]/GRID_SIZE[1])
GRID_COLOR = "black"

# # grid = [[None for x in range(GRID_SIZE[0])] for y in range(GRID_SIZE[1])]
# grid = pickle.load(open('save_level.pickle', 'rb'))


def main():
    is_running = True
    game_frame = frames.Game(WIN_SIZE, GRID_SIZE, GRID_SPACING)

    clock = pygame.time.Clock()
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
        
        game_frame.main(WIN)

    pygame.quit()


main()