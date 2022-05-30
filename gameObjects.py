import pygame
import os
import math

PLAYER_IMG = pygame.image.load(os.path.join("assets", "player.png"))
RECT_IMG = pygame.image.load(os.path.join("assets", "rect.png"))
CIRCLE_IMG = pygame.image.load(os.path.join("assets", "circle.png"))
COIN_IMG = pygame.image.load(os.path.join("assets", "coin.png"))

class Player:
    x_vel = 0
    y_vel = 0
    SPEED = 8

    def __init__(self, x, y, width, height):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.surface_path = ("assets", "player.png")

    def move_x(self, direction):
        self.x_vel = direction * self.SPEED

    def move_y(self, direction):
        self.y_vel = direction * self.SPEED

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.x_vel, self.y_vel = 0, 0

    def draw(self, win):
        win.blit(pygame.transform.scale(PLAYER_IMG, (self.width, self.height)), (self.x, self.y))

    def collide(self, obstacle):
        player_mask = pygame.mask.from_surface(PLAYER_IMG)
        obstacle_mask = obstacle.get_mask()
        offset = (obstacle.x - self.x, obstacle.y - round(self.y))
        point = player_mask.overlap(obstacle_mask, offset) # point of intercept

        if point: return True
        return False

    def check_radar(self, win, degree):
        len = 0
        self.center = (self.x + (self.width/2), self.y + (self.height/2))
        x = int(self.center[0] + math.cos(math.radians(degree))*len)
        y = int(self.center[1] + math.sin(math.radians(degree))*len)
        try:
            while win.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
                len += 1
                x = int(self.center[0] + math.cos(math.radians(degree))*len)
                y = int(self.center[1] + math.sin(math.radians(degree))*len)
        except: pass
            
        dist  = int(math.sqrt(math.pow(x-self.center[0], 2) + math.pow(y-self.center[1], 2)))
        return ((x, y), dist)

class Block:

    def __init__(self, x, y, width, height):
        self.width, self.height = width, height
        self.x, self.y = x, y

    def move(self):
        pass

    def draw(self, win):
        pass

class Simple_Block(Block):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.surface = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(pygame.transform.scale(RECT_IMG, (self.width, self.height)), (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(pygame.transform.scale(RECT_IMG, (self.width, self.height)))

class Moving_Block(Block):

    def __init__(self, x, y, width, height, direction, distance, speed=1):
        super().__init__(x, y, width, height)
        self.dest_x, self.dest_y = self.x, self.y
        self.start_x, self.start_y = self.x, self.y
        
        self.direction = direction
        self.distance = distance
        self.speed = speed/100

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
        step_x, step_y = (dx * self.speed, dy * self.speed)

        self.x += step_x
        self.y += step_y

        if abs(self.dest_x - self.x) <= abs(step_x) and abs(self.dest_y - self.y) <= abs(step_y):
            temp = (self.dest_x, self.dest_y)
            self.dest_x, self.dest_y = self.start_x, self.start_y
            self.start_x, self.start_y = temp
        
    def draw(self, win):
        win.blit(pygame.transform.scale(CIRCLE_IMG, (self.width, self.height)), (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(pygame.transform.scale(CIRCLE_IMG, (self.width, self.height)))


class Rotating_Block(Block):
    def blitRotateCenter(win, surface, topleft, angle):
        rotated_image = pygame.transform.rotate(surface, angle)
        new_rect = rotated_image.get_rect(center = surface.get_rect(topleft = topleft).center)

        win.blit(rotated_image, new_rect.topleft)

class Coin:
    def __init__(self, x, y, width, height):
        self.width, self.height = width, height
        self.x, self.y = x, y

    def draw(self, win):
        win.blit(pygame.transform.scale(COIN_IMG, (self.width, self.height)), (self.x, self.y))

    def move(self):
        pass

    def get_mask(self):
        return pygame.mask.from_surface(pygame.transform.scale(COIN_IMG, (self.width, self.height)))

    def get_rect(self):
        surf = pygame.transform.scale(COIN_IMG, (self.width*1.1, self.height*1.1))
        return surf.get_rect(center=(self.x+self.width/2, self.y+self.height/2))

class Button:
    def __init__(self, x, y, width, height, color, text, func=None):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.color = color
        self.text = text
        self.func = func

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def draw(self, win):
        self.surf.fill(self.color)

        font = pygame.font.SysFont("comicsans", int(self.width/len(self.text)))
        label = font.render(self.text, 1, (0,0,0))

        self.surf.blit(label, label.get_rect(center=[wh//2 for wh in (self.width, self.height)]))
        win.blit(self.surf, self.rect)

    def call_back(self, *args):
        if self.func:
            return self.func(*args)