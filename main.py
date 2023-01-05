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
from Scene import *
import random

pygame.init()


SCREEN_SCROLL = 0
BG_SCROLL = 0

######################################### Screen and Clock Initialization ############################################
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Glitch')
clock = pygame.time.Clock()

################################################## SCENE INITIALIZATION ###############################################

game_start = False 
Level_Select = False 

#################################################### GAME VARIABLES ##################################################
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
enemy_group =ENEMY_GROUP
enemy_bullet_group = pygame.sprite.Group()
item_box_group =  ITEM_BOX_GROUP
decoration_group = DECORATION_GROUP
water_group = WATER_GROUP
exit_group = EXIT_GROUP

################################################## INFILE FUNCTION ###################################################

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    DATA = []
    for row in range(ROWS):
        r = [-1] * COLS 
        DATA.append(r)

    return DATA

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



############################################# Instances  #############################################################

bg = Background(screen=screen)
world = World()
player, healthbar = world.process_delta(WORLD_DATA)
scene = Scene(screen)

################################################## MAIN DRIVER CODE ###################################################

print(enemy_group)
print(item_box_group)


################################################### GLITCH ############################################################
# Player Option Glitch
wall_bang_glitch = False 
teleport_glitch = False 

# Timer Glitch


GLITCH_LIST = {
    'No Glitch' : False,
    'control_glitch': False, 
    'direction_glitch': False, 
    'gravity_glitch': False 
}

glitch_happening = "No Glitch"
glitch_counter = 0

######### LEVEL TIMER #################################################
GLITCH_CLOCK = 360

run = True 
while run:
    # Settings
    clock.tick(FPS)

    if game_start == False:
        action = scene.home_screen()
        if action == 1:
            game_start = True 
        elif action == 2:
            run = False 
    else:
        #Background
        bg.draw_img_bg(bg_image, BG_SCROLL)

        world.draw(SCREEN_SCROLL)

        healthbar.draw_player(player.health, screen)
        # Text
        draw_text(f"Ammo: {player.ammo}", FONT, RED, 100, 35)
        draw_text(f"Grenades: {player.grenades}", FONT, RED, 100,55)
        draw_text(f"Health: {player.health}", FONT, RED, 100, 75)

        # Visualizing ammo and grenades

        for i in range(player.grenades):
            screen.blit(grenade_img, (135 + (i*20), 40))

        # Items Update
        item_box_group.update(player, SCREEN_SCROLL)
        item_box_group.draw(screen)

        water_group.update(SCREEN_SCROLL)
        water_group.draw(screen)

        exit_group.update(SCREEN_SCROLL)
        exit_group.draw(screen)

        decoration_group.update(SCREEN_SCROLL)
        decoration_group.draw(screen)

        #Enemy
        for enemy in enemy_group:
            healthbar.draw_enemy(enemy.health, screen, enemy)
            bullet = enemy.ai(player, world, SCREEN_SCROLL, BG_SCROLL, water_group, exit_group, GLITCH_LIST['control_glitch'], GLITCH_LIST['direction_glitch'], GLITCH_LIST['gravity_glitch'])
            if bullet:
                bullet_group.add(bullet)
            enemy.draw(screen)
            enemy.update()


        #Player
        player.draw(screen)
        player.update()

        #Bullet
        bullet_group.update(player, enemy_group, bullet_group, world, SCREEN_SCROLL)
        bullet_group.draw(screen)
    

        #Grenade
        
        grenade_group.update(player, enemy_group, world, SCREEN_SCROLL, GLITCH_LIST['direction_glitch'])
        grenade_group.draw(screen)
        

        #Animation
        explosion_group = EXPLOSION_GROUP
        explosion_group.update(SCREEN_SCROLL)
        explosion_group.draw(screen)

        ### Glitch
        glitch_action = scene.ingame_ui(GLITCH_CLOCK // FPS, glitch_happening)

        ########################## GLITCH VALUES ####################################
        glitch_types = list(GLITCH_LIST.keys())
    
        #################### CONTROLLING GLITCH ########################################

        if GLITCH_CLOCK == 0:
            GLITCH_LIST = {
                'control_glitch': False, 
                'direction_glitch': False, 
                'gravity_glitch': False 
            }
            glitch_happening = glitch_types[glitch_counter]
            GLITCH_LIST[glitch_happening] = True 
            glitch_counter += 1
            if glitch_counter >= len(glitch_types):
                glitch_counter = 0
        if GLITCH_CLOCK <= 0:
            GLITCH_CLOCK = random.randint(6, 16)*FPS #TASK: eta ke random korte hobe 
        GLITCH_CLOCK -= 1

        ################# GLITCH BUTTON ##############################################

        
         

        # Shooring anmd moving 
        if player.alive:

            if shoot:
                bullet = player.shoot(bullet_img, GLITCH_LIST['direction_glitch'])
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

            SCREEN_SCROLL, level_complete = player.move(moving_left, moving_right, world, BG_SCROLL, water_group, exit_group, GLITCH_LIST['control_glitch'], GLITCH_LIST['gravity_glitch'])
            BG_SCROLL -= SCREEN_SCROLL

            if level_complete:
                LEVEL += 1
                BG_SCROLL = 0
                world_data = reset_level()
                if LEVEL <= MAX_LEVELS:
                    with open(f'level{LEVEL}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                        world = World()
                        player, healthbar = world.process_delta(world_data)
                wall_bang_glitch = False 
                wet_glitch = False 
                teleport_glitch = False 
                GLITCH_CLOCK = 360

                # Timer Glitch
                GLITCH_LIST = {
                    'control_glitch': False, 
                    'direction_glitch': False, 
                    'gravity_glitch': False 
                }
                glitch_happening = "No Glitch"
                glitch_counter = 0
                

        else:
            action = scene.restart_screen()
            if action == 1:
                BG_SCROLL = 0
                world_data = reset_level()

                with open(f'level{LEVEL}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, healthbar = world.process_delta(world_data)
                # Player Option Glitch
                wall_bang_glitch = False 
                wet_glitch = False 
                teleport_glitch = False 
                GLITCH_CLOCK = 360

                # Timer Glitch
                GLITCH_LIST = {
                    'control_glitch': False, 
                    'direction_glitch': False, 
                    'gravity_glitch': False 
                }
                glitch_happening = "No Glitch"
                glitch_counter = 0
                            

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

            if event.key == pygame.K_s and player.alive and GLITCH_LIST['gravity_glitch']:
                player.down_jump = True 

            


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