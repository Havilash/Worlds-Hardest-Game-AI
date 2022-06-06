import enum
import math
from turtle import color
import pygame
import gameObjects
import pickle
import neat


pygame.init()
gen = 0
num = 1

class Frame:
    def __init__(self, win_size, grid_size, grid_spacing):
        self.grid = None
        self.WIN_SIZE, self.GRID_SIZE, self.GRID_SPACING = win_size, grid_size, grid_spacing

    def draw_grid(self, win, grid_color):
        for x in range(self.GRID_SIZE[0]):
            pygame.draw.rect(win, grid_color, pygame.Rect(x*self.GRID_SPACING[0], 0, 1, self.WIN_SIZE[1]))
        for y in range(self.GRID_SIZE[1]):
            pygame.draw.rect(win, grid_color, pygame.Rect(0, y*self.GRID_SPACING[1], self.WIN_SIZE[0], 1))

    def draw_objects(self, win):
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj:
                    obj.draw(win)

    def draw(self, win):
        pass

    def check_events(self, win, event):
        pass

    def main(self, win):
        pass


class Game(Frame):

    def __init__(self, genomes, config, win_size, grid_size, grid_spacing):
        super().__init__(win_size, grid_size, grid_spacing)
        self.grid = pickle.load(open('save_level.pickle', 'rb'))
        self.winner = None
        try: self.winner = pickle.load(open('winner.pickle', 'rb'))
        except: print("No Winner")

        global gen
        gen += 1


        self.kill_btn = gameObjects.Button(40, 20, 60, 30, 'red', "Kill", self.kill_btn_func)

        self.main_player_grid_pos, self.main_player = self.get_object(gameObjects.Player)
        self.main_player_grid_pos, self.main_player = self.main_player_grid_pos[0], self.main_player[0]

        self.coins_grid_pos, self.coins = self.get_object(gameObjects.Coin)

        self.genomes = genomes
        self.config = config
        self.radars = []

        self.players = []
        self.ge = []
        self.nets = []

        for genome_id, genome in self.genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.players.append(gameObjects.Player(self.main_player_grid_pos[0]*self.GRID_SPACING[0], self.main_player_grid_pos[1]*self.GRID_SPACING[1], self.GRID_SPACING[0]/1.15, self.GRID_SPACING[1]/1.15))
            self.ge.append(genome)

        self.players_coins_state = []
        for i, player in enumerate(self.players):
            tmp_dict = {}
            for j, coin in enumerate(self.coins):
                tmp_dict[(self.coins_grid_pos[j][0], self.coins_grid_pos[j][1])] = False
            self.players_coins_state.append(tmp_dict)


    def get_object(self, object_type):
        objs = []
        pos = []
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: 
                    if type(obj) == object_type: 
                        pos.append((x, y))
                        objs.append(obj)
        return (pos, objs)
                        

    def draw_objects(self, win):
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj and not type(obj) == gameObjects.Player:
                    obj.draw(win)


    def draw(self, win, obstacle_win):
        obstacle_win.fill("white")
        win.fill("white")

        self.draw_grid(win, 'black')
        self.draw_objects(obstacle_win)
        win.blit(obstacle_win, (0, 0))

        if len(self.players) > 0:
            for j, pos in enumerate(self.radars[0]):
                pos = pos[0]
                if self.is_coin[0][j] == 1: color = 'red'
                else: color = 'black'
                pygame.draw.line(win, color, self.players[0].center, pos)

        for player in self.players:
            player.draw(win)

        self.kill_btn.draw(win)

        pygame.display.update()

    def kill_btn_func(self):
        self.nets = []
        self.ge = []
        self.players = []

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.kill_btn.rect.collidepoint(pos):
                self.kill_btn.call_back()

    def main(self, win, obstacle_win):
        # get radar data
        self.radars = [[] for i in range(len(self.players))]
        for i, player in enumerate(self.players):
            for degree in range(0, 360, 5):
                self.radars[i].append(player.check_radar(obstacle_win, degree, self.players_coins_state))
        

        self.is_coin = [[] for i in range(len(self.players))]
        for i in range(len(self.players)):
            for pos in [self.radars[i][j][0] for j in range(len(self.radars[i]))]:
                tmp_is_coin = 0
                for coin in self.coins:
                    if coin.get_rect().collidepoint(pos):
                        tmp_is_coin = 1
                self.is_coin[i].append(tmp_is_coin)

        # evaluate data
        for i, player in enumerate(self.players):
            self.ge[i].fitness -= 0.02

            radar_data = [self.radars[i][j][1] for j in range(len(self.radars[i]))]
        
            output = self.nets[i].activate((*radar_data, *self.is_coin[i]))

            if output[0] > 0.5:
                player.move_y(-1)
                self.ge[i].fitness += 0.01
            if output[1] > 0.5:
                player.move_y(1)
                self.ge[i].fitness += 0.01
            if output[2] > 0.5:
                player.move_x(-1)
                self.ge[i].fitness += 0.01
            if output[3] > 0.5:
                player.move_x(1)
                self.ge[i].fitness += 0.01



        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: 
                    obj.move()

                    for i, player in enumerate(self.players):
                        player.move()

                        if type(obj) != gameObjects.Player:
                            if player.collide(obj):
                                if type(obj) == gameObjects.Coin:
                                    if not self.players_coins_state[i][(x, y)]:
                                        self.ge[i].fitness += 5
                                        # self.players_coins_state[i][(x, y)] = True
                                        self.grid[y][x] = None
                                else:
                                    self.ge[i].fitness -= 3
                                    self.nets.pop(i)
                                    self.ge.pop(i)
                                    self.players.pop(i)
                                    self.is_coin.pop(i)

        # for key in self.players_coins_state[0]:
        #     tmp_bool = True
        #     for i in range(len(self.players_coins_state)):
        #         if not self.players_coins_state[i][key]:
        #             tmp_bool = False
        #             break
        #     if tmp_bool:
        #         self.grid[key[0]][key[1]] = None

        for i, player in enumerate(self.players):
            if self.ge[i].fitness < 0:
                self.nets.pop(i)
                self.ge.pop(i)
                self.players.pop(i)
                self.is_coin.pop(i)


        self.draw(win, obstacle_win)

        if len(self.players)>0:
            if self.ge[0].fitness > 100:
                pickle.dump(self.nets[0], open("winner.pickle", 'wb'))

        global num, gen
        if gen >= 15 * num:
            if len(self.players) > 0:
                num += 1
                pickle.dump(self.nets[0], open("crnt_winner.pickle", 'wb'))
                print("[SAVING] ...")



class Level_Creator(Frame):

    STAT_FONT = pygame.font.SysFont("comicsans", 20)
    STAT_FONT_SMALL = pygame.font.SysFont("comicsans", 15)

    obj_names = ['Nothing', 'Simple Block', 'Moving Block', 'Rotating Block', 'Coin', 'Player']
    crnt_obj = 0
    direction_names = ['n', 'e', 's', 'w']
    crnt_direction = 0
    distance = 1
    block_speed = 1
    changing_status = 0

    def __init__(self, win_size, grid_size, grid_spacing):
        super().__init__(win_size, grid_size, grid_spacing)
        self.grid = [[gameObjects.Simple_Block(x*self.GRID_SPACING[0], y*self.GRID_SPACING[1], *self.GRID_SPACING) for x in range(self.GRID_SIZE[0])] for y in range(self.GRID_SIZE[1])]
        self.grid = pickle.load(open('save_level.pickle', 'rb'))

    def set_object(self, x, y, obj):
        self.grid[y][x] = obj

    def draw(self, win):
        win.fill("white")

        self.draw_grid(win, 'black')
        self.draw_objects(win)

        # Objects
        obj_names_label = self.STAT_FONT.render(self.obj_names[self.crnt_obj], 1, (0,0,0))
        win.blit(obj_names_label, (self.WIN_SIZE[0] - obj_names_label.get_width() - 20, 10))

        # Object --> Moving Block
        if self.obj_names[self.crnt_obj] == 'Moving Block':
            color = (0,0,0)
            # Direction
            if self.changing_status == 0: color = 'dark red' 
            else: color = (0,0,0)
            direction_names_label = self.STAT_FONT_SMALL.render("Direction: " + self.direction_names[self.crnt_direction].upper(), 1, color)
            win.blit(direction_names_label, (self.WIN_SIZE[0] - obj_names_label.get_width() - 20, 10+obj_names_label.get_height()))
            # Distance
            if self.changing_status == 1: color = 'dark red' 
            else: color = (0,0,0)
            distance_label = self.STAT_FONT_SMALL.render("Distance: " + str(self.distance), 1, color)
            win.blit(distance_label, (self.WIN_SIZE[0] - obj_names_label.get_width() - 20, 10+obj_names_label.get_height()+direction_names_label.get_height()))
            # Speed
            if self.changing_status == 2: color = 'dark red' 
            else: color = (0,0,0)
            speed_label = self.STAT_FONT_SMALL.render("Speed: " + str(self.block_speed), 1, color)
            win.blit(speed_label, (self.WIN_SIZE[0] - obj_names_label.get_width() - 20, 10+obj_names_label.get_height()+direction_names_label.get_height()+distance_label.get_height()))

        pygame.display.update()

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.obj_names[self.crnt_obj] == 'Moving Block':
                if self.changing_status == 0:
                    if event.key == pygame.K_UP: self.crnt_direction += 1
                    if event.key == pygame.K_DOWN: self.crnt_direction -= 1
                elif self.changing_status == 1:
                    if event.key == pygame.K_UP: self.distance += 1
                    if event.key == pygame.K_DOWN: self.distance -= 1
                elif self.changing_status == 2:
                    if event.key == pygame.K_UP: self.block_speed += 1
                    if event.key == pygame.K_DOWN: self.block_speed -= 1

            if event.key == pygame.K_TAB:
                self.changing_status += 1
                if self.changing_status > 2: self.changing_status = 0
                if self.changing_status < 0: self.changing_status = 2

            if event.key == pygame.K_RIGHT:
                self.crnt_obj += 1

            if event.key == pygame.K_LEFT:
                self.crnt_obj -= 1

    def main(self, win):
        if self.crnt_obj >= len(self.obj_names): self.crnt_obj = 0
        if self.crnt_obj < 0: self.crnt_obj = len(self.obj_names)-1
        if self.crnt_direction >= len(self.direction_names): self.crnt_direction = 0
        if self.crnt_direction < 0: self.crnt_direction = len(self.direction_names)-1

        # Place Objects
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (int(mouse_pos[0]/self.GRID_SPACING[0]), int(mouse_pos[1]/self.GRID_SPACING[1]))
            surface = None
            if self.obj_names[self.crnt_obj] == 'Nothing': surface = None
            elif self.obj_names[self.crnt_obj] == 'Simple Block': surface = gameObjects.Simple_Block(mouse_pos[0]*self.GRID_SPACING[0], mouse_pos[1]*self.GRID_SPACING[1], *self.GRID_SPACING)
            elif self.obj_names[self.crnt_obj] == 'Moving Block': surface = gameObjects.Moving_Block(mouse_pos[0]*self.GRID_SPACING[0], mouse_pos[1]*self.GRID_SPACING[1], *self.GRID_SPACING, self.direction_names[self.crnt_direction], self.distance*self.GRID_SPACING[0], self.block_speed)
            if self.obj_names[self.crnt_obj] == 'Rotating Block': surface = None
            if self.obj_names[self.crnt_obj] == 'Coin': surface = gameObjects.Coin(mouse_pos[0]*self.GRID_SPACING[0], mouse_pos[1]*self.GRID_SPACING[1], self.GRID_SPACING[0]/1.5, self.GRID_SPACING[1]/1.5)
            if self.obj_names[self.crnt_obj] == 'Player': surface = gameObjects.Player(mouse_pos[0]*self.GRID_SPACING[0], mouse_pos[1]*self.GRID_SPACING[1], self.GRID_SPACING[0]/1.15, self.GRID_SPACING[1]/1.15)
            self.set_object(*mouse_pos, surface)

        # Save Level
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
            pickle.dump(self.grid, open('save_level.pickle', 'wb'))
        
        for y in range(len(self.grid)):
            for x, obj in enumerate(self.grid[y]):
                if obj: obj.move()

        self.draw(win)