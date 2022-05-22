import pygame
from sympy import principal_branch
import gameObjects

pygame.init()

WIN_SIZE = (1000, 800)
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("World Hardest Game")
FPS = 30

GRID_SIZE = (25, 20)
GRID_SPACING = (WIN_SIZE[0]/GRID_SIZE[0], WIN_SIZE[1]/GRID_SIZE[1])
GRID_COLOR = "black"

grid = [[None for x in range(GRID_SIZE[0])] for y in range(GRID_SIZE[1])]
grid[5][5] = gameObjects.Moving_Block(5*GRID_SPACING[0], 5*GRID_SPACING[1], *GRID_SPACING, "e")



def draw_grid(win):
    for x in range(GRID_SIZE[0]):
        pygame.draw.rect(win, GRID_COLOR, pygame.Rect(x*GRID_SPACING[0], 0, 1, WIN_SIZE[1]))
    for y in range(GRID_SIZE[1]):
        pygame.draw.rect(win, GRID_COLOR, pygame.Rect(0, y*GRID_SPACING[1], WIN_SIZE[0], 1))


def set_object(x, y, obj):
    print(x, y)
    grid[x][y] = obj


def draw_objects(win):
    for y in range(len(grid)):
        for x, obj in enumerate(grid[y]):
            if obj: 
                obj.draw(win)


def draw(win):
    win.fill("white")

    draw_grid(win)
    draw_objects(win)

    pygame.display.update()


def main():
    is_running = True

    clock = pygame.time.Clock()
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (int(mouse_pos[0]/GRID_SPACING[0]), int(mouse_pos[1]/GRID_SPACING[1]))
                set_object(*mouse_pos, gameObjects.Simple_Block(mouse_pos[0]*GRID_SPACING[0], mouse_pos[1]*GRID_SPACING[1], *GRID_SPACING))
                set_object(*mouse_pos, gameObjects.Moving_Block(mouse_pos[0]*GRID_SPACING[0], mouse_pos[1]*GRID_SPACING[1], *GRID_SPACING, "e"))

        
        for y in range(len(grid)):
            for x, obj in enumerate(grid[y]):
                if obj: obj.move()

        draw(WIN)

    pygame.quit()


main()