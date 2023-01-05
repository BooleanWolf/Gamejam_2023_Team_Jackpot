import pygame 
from ImageGraphics import *
from Settings import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(f'./assets/Weapons/Explosion/exp{i}.png').convert_alpha()
            img = transform_image(img, EXPLOSION_SCALE)
            self.images.append(img)
        
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL 
        EXPLOSION_SPEED = 6

        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0

            self.frame_index += 1

            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.frame_index = len(self.images) - 1
                
                self.image = self.images[self.frame_index]

            
       