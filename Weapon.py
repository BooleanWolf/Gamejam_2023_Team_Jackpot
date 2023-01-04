import pygame 
from Settings import *
from Animation import *

EXPLOSION_GROUP = pygame.sprite.Group()



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, player, enemy_group, bullet_group):
        self.rect.x += (self.direction * self.speed) 

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 10
                print(f"Player Health: {player.health}")
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    print(f"Enemy Health: {enemy.health}")
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -11
        self.speed = 7
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, player, enemy_group):
        self.velocity_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.velocity_y

        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom 
            dx = 0
        
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx 
        self.rect.y += dy

        self.timer  -= 1
        a = 0
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y)
            EXPLOSION_GROUP.add(explosion)
        
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and  abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
                print(player.health)
            
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and  abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 30
                    print(enemy.health)



           


        