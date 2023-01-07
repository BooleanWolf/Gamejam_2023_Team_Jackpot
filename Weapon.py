import pygame 
from Settings import *
from Animation import *
from Audio import *

EXPLOSION_GROUP = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, not_glitch):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.not_glitch = not_glitch
    
    def update(self, player, enemy_group, bullet_group, world, SCREEN_SCROLL, wallbang_glitch):
      
        self.rect.x += (self.not_glitch * self.direction * self.speed) + SCREEN_SCROLL

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # Glitch 2 : Wall Bang - Bullets will go through the wall (Remove the next three lines)
        if not wallbang_glitch:
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

        
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                getting_hit_fx.play()
                player.health -= 5
                
                print(f"Player Health: {player.health}")
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 20
                    player.level_score += 2
                    print(f"Enemy Health: {enemy.health}")
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -8
        self.speed = 5
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update(self, player, enemy_group, world,SCREEN_SCROLL, direction_glitch):
        self.velocity_y += GRAVITY

        if direction_glitch:
            dx = -self.direction * self.speed
        else:
            dx = self.direction * self.speed

        dy = self.velocity_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top 
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    dy = tile[1].top - self.rect.bottom 

       

        self.rect.x += dx  + SCREEN_SCROLL
        self.rect.y += dy

        self.timer  -= 1
        a = 0
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y)
            EXPLOSION_GROUP.add(explosion)
        
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and  abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                getting_hit_fx.play()
                player.health -= 45
                
                print(player.health)
            
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and  abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 45
                    player.level_score += 5
                    print(enemy.health)



           


        