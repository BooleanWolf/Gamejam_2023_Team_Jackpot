import pygame
from Settings import * 
from ImageGraphics import *

item_boxes = {
    'HEALTH' : health_box,
    'AMMO' : ammo_box,
    'GRENADE' : grenade_box
}

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,x,y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "HEALTH":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "AMMO":
                player.ammo += 5
            elif self.item_type == "GRENADE":
                player.grenades += 1
            
            self.kill()
            
            print(player.health, player.grenades, player.ammo)



