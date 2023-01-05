import pygame
import csv 
from Settings import *
from ImageGraphics import *
from Character import *
from Items import *
from Graphics import *

ENEMY_GROUP = pygame.sprite.Group()
ITEM_BOX_GROUP =  pygame.sprite.Group()
DECORATION_GROUP = pygame.sprite.Group()
EXIT_GROUP = pygame.sprite.Group()
WATER_GROUP = pygame.sprite.Group()

WORLD_DATA = []
for row in range(ROWS):
    r = [-1] * COLS 
    WORLD_DATA.append(r)

with open(f'level{LEVEL}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            WORLD_DATA[x][y] = int(tile)

class World:
    def __init__(self):
        self.obstacle_list = []

    def process_delta(self, data):


        self.level_length = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = TILES_IMG_LIST[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        WATER_GROUP.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        DECORATION_GROUP.add(decoration)
                    elif tile == 15:
                        player = Character(x = x * TILE_SIZE, y = y * TILE_SIZE, char_type="Player",type = PLAYER_TYPE, scale= 0.2,speed= 5, ammo=5, grenades=10)
                        healthbar = HealthBar(10, 10, player.health, player.max_health)
                    elif tile == 16:
                        enemy = Character(x = x * TILE_SIZE, y = y * TILE_SIZE, char_type="Enemy", type="CuteBorg", scale=0.25, speed=3, ammo=5, grenades=0)
                        ENEMY_GROUP.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'AMMO')
                        ITEM_BOX_GROUP.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'GRENADE')
                        ITEM_BOX_GROUP.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'HEALTH')
                        ITEM_BOX_GROUP.add(item_box)
                    elif tile == 20: # Exit 
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        EXIT_GROUP.add(exit)
        return player, healthbar
    
    def draw(self, SCREEN_SCROLL):
        for tile in self.obstacle_list:
            tile[1][0] += SCREEN_SCROLL 
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y+ (TILE_SIZE - self.image.get_height()))
    
    def update(self, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL

class Water(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y+ (TILE_SIZE - self.image.get_height()))
    
    def update(self, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL

class Exit(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y+ (TILE_SIZE - self.image.get_height()))

    def update(self, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL