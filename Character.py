from ImageGraphics import *
import pygame 
from Weapon import *
from Settings import *
import random

import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, type, ammo, grenades ,scale = 1, speed = 1):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True 

        self.direction = 1
        self.flip = False 

        self.char_type = char_type
        self.type = type

        self.speed = speed
        self.x = x
        self.y = y

        self.jump = False 
        self.vel_y = 0

        self.scale = scale

        self.in_air = True 

        self.shoot_cooldown = 0

        self.ammo = ammo
        self.start_ammo = ammo

        self.grenades = grenades
        self.max_grenades = grenades

        self.health = 100
        self.max_health = self.health
     
        self.animation_list = []
        self.frame_index = 0 
        temp_list = []
        # 0 - Idle 1 - Run 2 - Attack 3 - Run and Attack 
        self.action = 0

        self.move_counter = 0
        self.idling = False 
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

        # Glitch
        self.down_jump = False 

        if self.char_type == "Player":
            temp_list = []
            for i in range(4):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Idle_{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)
            
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(6):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Run_{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)
            
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(6):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Attack_{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)

            self.animation_list.append(temp_list)

        if self.char_type == "Enemy":
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Idle/{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)
            
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(6):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Run/{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)
            
            self.animation_list.append(temp_list)
            
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f"./assets/Characters/{self.char_type}/{self.type}/Death/{i}.png").convert_alpha()
                img = transform_image(img, self.scale)
                temp_list.append(img)
            
            self.animation_list.append(temp_list)

        self.update_time = pygame.time.get_ticks()

        self.img = self.animation_list[self.action][self.frame_index]
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
        # Pointing System
        self.score = 0
        self.level_score = 0

    
    def update(self):
        self.update_animation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        self.check_alive()
        
    
    def move(self, moving_left, moving_right, world, bg_scroll, water_group, exit_group, control_glitch, gravity_glitch, teleport_glitch):
        dx = dy = 0
        SCREEN_SCROLL = 0

        if control_glitch and self.char_type == "Player":
            if moving_right:
                dx = -self.speed
                self.direction = -1
                self.flip = True 
            if moving_left:
                dx = self.speed
                self.direction = 1
                self.flip = False  
        else:
            if moving_left:
                dx = -self.speed
                self.direction = -1
                self.flip = True 
            if moving_right:
                dx = self.speed
                self.direction = 1
                self.flip = False  
        
        # GRAVITY = 0.2
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False 
            self.in_air = True 
        
        if self.down_jump == True:
            self.vel_y = 12
            self.down_jump = False 

        if self.char_type == "Player" and gravity_glitch:
            gravity = 0.2 
            self.vel_y += -gravity
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y
        else:
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

        # Check Collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

                if self.char_type == 'Enemy':
                    self.direction += -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if not teleport_glitch:
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top 
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False 
                        dy = tile[1].top - self.rect.bottom 
                else:
                # Glitch 1 : "Player will teleport to the above bar"                
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top 
                    if self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False 
                        dy = tile[1].top - self.rect.bottom 

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        level_complete = False 
        if pygame.sprite.spritecollide(self, exit_group, False) and self.level_score >= NEXT_LEVEL_PASS:
            level_complete = True 
        
        


        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0



        if self.char_type == "Player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
            
            if self.rect.top + dy <= 0:
                dy = 0
                self.alive = False 

        
        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == "Player":
            if( self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or( self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                SCREEN_SCROLL = -dx 

        return SCREEN_SCROLL, level_complete
    
    def shoot(self, bullet_img, direction_glitch):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            
            if self.char_type == "Player" and direction_glitch:
                if self.direction == 1:
                    flip_bullet_img = flip_image_x(bullet_img)
                    bullet = Bullet(self.rect.centerx + (-self.direction*0.75* self.rect.size[0]), self.rect.centery, self.direction, flip_bullet_img, -1)
                    self.ammo -= 1
                    return bullet
                if self.direction == -1:
                    bullet = Bullet(self.rect.centerx + (-self.direction*0.75* self.rect.size[0]), self.rect.centery, self.direction, bullet_img, -1)
                    self.ammo -= 1
                    return bullet
            else:
                if self.direction == 1:
                    bullet = Bullet(self.rect.centerx + (self.direction*0.75* self.rect.size[0]), self.rect.centery, self.direction, bullet_img, 1)
                    self.ammo -= 1
                    return bullet
                if self.direction == -1:
                    flip_bullet_img = flip_image_x(bullet_img)
                    bullet = Bullet(self.rect.centerx + (self.direction*0.75* self.rect.size[0]), self.rect.centery, self.direction, flip_bullet_img, 1)
                    self.ammo -= 1
                    return bullet
            
    def ai(self, player, world, SCREEN_SCROLL, bg_scroll, water_group, exit_group, control_glitch, direction_glitch,  gravity_glitch, teleport_glitch):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 50) == 5:
                self.idling= True
                self.idling_counter = 50
                self.update_action(0)
            
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                return self.shoot(bullet_img, direction_glitch)
                



            if self.idling == False:
                ai_moving_right = False 
                if self.direction == 1:
                    ai_moving_right = True 
                else:
                    ai_moving_right = False 
                
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right, world, bg_scroll, water_group, exit_group, control_glitch,  gravity_glitch, teleport_glitch)
                self.update_action(1)
                self.move_counter += 1

                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
               

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False 
        
        self.rect.x += SCREEN_SCROLL



    def update_animation(self):
        ANIMATION_COOLDOWN = 150

        self.img = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if not (self.char_type == "Enemy" and self.action == 2):
                self.frame_index = 0 
            else:
                self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def check_alive(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False 
            self.update_action(2)
        
        return self.alive
    
  

    def draw(self, screen):
        img = pygame.transform.flip(self.img, self.flip, False)
        screen.blit(img, self.rect)
