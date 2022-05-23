import pygame
import gameObjects
import pickle

WIN_SIZE = (1000, 800)
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("World Hardest Game")
FPS = 60

GRID_SIZE = (25, 20)
GRID_SPACING = (WIN_SIZE[0]/GRID_SIZE[0], WIN_SIZE[1]/GRID_SIZE[1])
GRID_COLOR = "black"


class Game:

    def __init__(self, win):
        self.grid = pickle.load(open('save_level.pickle', 'rb'))
        self.win = win


    def draw(self, win):
        win.fill("white")

        # self.draw_grid(win)
        # self.draw_objects(win)

        pygame.display.update()


    def main(self):        
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: obj.move()

        self.draw(self.win)



def main():
    is_running = True
    test = Game()

    clock = pygame.time.Clock()
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
        
        test.main()

    pygame.quit()

main()