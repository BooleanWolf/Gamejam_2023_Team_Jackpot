from ImageGraphics import *
from Graphics import *
from Weapon import *
import pygame 
from Settings import *
from Character import *
import json
from Animation import *
from Items import *
from World import *
from Instances import *
import csv


pygame.init()
######################################### Screen and Clock Initialization ############################################
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Glitch')
clock = pygame.time.Clock()


################################################## INFILE FUNCTION ###################################################

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

################################################## JSON File #########################################################

variables = {
    "PLAYER_TYPE" : "Cyborg",
    "High Score" : 0
}

json_obj = json.dumps(variables, indent=4)

with open("local_variable.json", "w") as outfile:
    outfile.write(json_obj)

################################################## Player Action #####################################################
moving_left = moving_right = shoot = grenade = False
grenade_thrown = False 

#################################################### GAME VARIABLES ##################################################
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
enemy_group =ENEMY_GROUP
enemy_bullet_group = pygame.sprite.Group()
item_box_group =  ITEM_BOX_GROUP
decoration_group = DECORATION_GROUP
water_group = WATER_GROUP
exit_group = EXIT_GROUP

############################################# Instances  #############################################################

bg = Background(screen=screen)
world = World()
player, healthbar = world.process_delta(WORLD_DATA)


################################################## MAIN DRIVER CODE ###################################################

print(enemy_group)
print(item_box_group)

run = True 
while run:
    # Settings
    clock.tick(FPS)

    #Background
    bg.draw_simple_bg()

    world.draw()

    healthbar.draw_player(player.health, screen)

   

    # Text
    draw_text(f"Ammo: {player.ammo}", FONT, RED, 100, 35)
    draw_text(f"Grenades: {player.grenades}", FONT, RED, 100,55)
    draw_text(f"Health: {player.health}", FONT, RED, 100, 75)

    # Visualizing ammo and grenades

    for i in range(player.grenades):
        screen.blit(grenade_img, (135 + (i*20), 40))

    # Items Update
    item_box_group.update(player)
    item_box_group.draw(screen)

    water_group.update()
    water_group.draw(screen)

    exit_group.update()
    exit_group.draw(screen)

    decoration_group.update()
    decoration_group.draw(screen)

    #Enemy
    for enemy in enemy_group:
        bullet = enemy.ai(player)
        if bullet:
            bullet_group.add(bullet)
        enemy.draw(screen)
        enemy.update()


    #Player
    player.draw(screen)
    player.update()

    #Bullet
    bullet_group.update(player, enemy_group, bullet_group)
    bullet_group.draw(screen)
  

    #Grenade
    
    grenade_group.update(player, enemy_group)
    grenade_group.draw(screen)
    

    #Animation
    explosion_group = EXPLOSION_GROUP
    explosion_group.update()
    explosion_group.draw(screen)


    


    # Shooring anmd moving 
    if player.alive:

        if shoot:
            bullet = player.shoot(bullet_img)
            if bullet:
                bullet_group.add(bullet)
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction), player.rect.top, player.direction, grenade_img)
            grenade_group.add(grenade)
            grenade_thrown = True 
            player.grenades -= 1
        
      


        if moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)

        player.move(moving_left, moving_right)


    
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        # Pressing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True 
            if event.key == pygame.K_d:
                moving_right = True 
            if event.key == pygame.K_SPACE:
                shoot = True 
            if event.key == pygame.K_q:
                grenade = True 
            if event.key == pygame.K_w and player.alive:
                player.jump = True 

            


            if event.key == pygame.K_ESCAPE:
                run = False 
        
        # Releasing
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False 
            if event.key == pygame.K_d:
                moving_right = False 
            if event.key == pygame.K_SPACE:
                shoot = False 
            if event.key == pygame.K_q:
                grenade = False 
                grenade_thrown = False



    pygame.display.update()