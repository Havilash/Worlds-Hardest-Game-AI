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
        pygame.draw.rect(win, self.COLOR, self.surface)

    def get_mask(self):
        pygame.mask.from_surface(self.surface)

class Simple_Block(Block):
    COLOR = "blue"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.surface = pygame.Rect(self.x, self.y, self.width, self.height)


class Moving_Block(Block):
    COLOR = "red"

    def __init__(self, x, y, width, height, direction, distance, speed=10):
        super().__init__(x, y, width, height)
        self.dest_x, self.dest_y = self.x, self.y
        self.start_x, self.start_y = self.x, self.y
        
        self.direction = direction
        self.distance = distance
        self.speed = speed

        if self.direction == 'n':
            self.dest_y -= self.distance
        elif self.direction == 'e':
            self.dest_x += self.distance
        elif self.direction == 's':
            self.dest_y += self.distance
        elif self.direction == 'w':
            self.dest_x -= self.distance

    def move(self):
        dx, dy = (self.dest_x - self.start_x, self.dest_y - self.start_y)
        step_x, step_y = (dx / self.speed, dy / self.speed)

        self.x += step_x
        self.y += step_y

        if abs(self.dest_x - self.x) <= 0 and abs(self.dest_y - self.y) <= 0:
            temp = (self.dest_x, self.dest_y)
            self.dest_x, self.dest_y = self.start_x, self.start_y
            self.start_x, self.start_y = temp
        
    def draw(self, win):
        radius = self.width/2.5
        pygame.draw.circle(win, self.COLOR, (self.x + self.width/2, self.y + self.width/2), radius)

class Rotating_Block(Block):
    def blitRotateCenter(win, surface, topleft, angle):
        rotated_image = pygame.transform.rotate(surface, angle)
        new_rect = rotated_image.get_rect(center = surface.get_rect(topleft = topleft).center)

        win.blit(rotated_image, new_rect.topleft)