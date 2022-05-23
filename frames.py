import pygame
from sympy import frac
import gameObjects
import pickle

class Frame:
    def __init__(self, win_size, grid_size, grid_spacing):
        self.grid = None
        self.win_size, self.grid_size, self.grid_spacing = win_size, grid_size, grid_spacing

    def draw_grid(self, win, grid_color):
        for x in range(self.grid_size[0]):
            pygame.draw.rect(win, grid_color, pygame.Rect(x*self.grid_spacing[0], 0, 1, self.win_size[1]))
        for y in range(self.grid_size[1]):
            pygame.draw.rect(win, grid_color, pygame.Rect(0, y*self.grid_spacing[1], self.win_size[0], 1))

    def draw_objects(self, win):
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: 
                    obj.draw(win)

    def draw(self, win):
        pass

    def main(self, win):
        pass


class Game(Frame):

    def __init__(self, win_size, grid_size, grid_spacing):
        super().__init__(win_size, grid_size, grid_spacing)
        self.grid = pickle.load(open('save_level.pickle', 'rb'))
        
    def draw(self, win):
        win.fill("white")

        self.draw_grid(win, 'black')
        self.draw_objects(win)

        pygame.display.update()


    def main(self, win):        
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: obj.move()

        self.draw(win)


class Level_Creator(Frame):
    
    def __init__(self, win_size, grid_size, grid_spacing):
        super().__init__(win_size, grid_size, grid_spacing)

    def draw(self, win):
        pass

    def main(self, win):
        pass