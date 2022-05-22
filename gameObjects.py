import pygame


class Player:
    pass


class Block:
    def __init__(self, x, y, width, height):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.surface = None

    def move(self):
        pass

    def draw(self, win):
        self.surface = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.COLOR, self.surface)

    def get_mask(self):
        pygame.mask.from_surface(self.surface)

class Simple_Block(Block):
    COLOR = "blue"

class Moving_Block(Block):
    COLOR = "red"
    DISTANCE = 5
    SPEED = 8

    def __init__(self, x, y, width, height, direction):
        super().__init__(x, y, width, height)
        self.DISTANCE *= width
        self.dest_x, self.dest_y = self.x, self.y
        self.start_x, self.start_y = self.x, self.y
        self.direction = direction

        if self.direction == 'n':
            self.dest_y -= self.DISTANCE
        elif self.direction == 'e':
            self.dest_x += self.DISTANCE
        elif self.direction == 's':
            self.dest_y += self.DISTANCE
        elif self.direction == 'w':
            self.dest_x -= self.DISTANCE

    def move(self):
        if self.direction == 'n':
            self.y -= self.SPEED
        elif self.direction == 'e':
            self.x += self.SPEED
        elif self.direction == 's':
            self.y += self.SPEED
        elif self.direction == 'w':
            self.x -= self.SPEED

        if (self.y == self.dest_y and self.x == self.dest_x) or (self.y == self.start_y and self.x == self.start_x):
            self.SPEED *= -1
        

class Rotating_Block(Block):
    pass