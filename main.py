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

play = False 
game_start = False 
how_to_Scene = False 

#################################################### GAME VARIABLES ##################################################
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
enemy_group =ENEMY_GROUP
enemy_bullet_group = pygame.sprite.Group()
item_box_group =  ITEM_BOX_GROUP
decoration_group = DECORATION_GROUP
water_group = WATER_GROUP
exit_group = EXIT_GROUP
money_group = MONEY_GROUP
explosion_group = EXPLOSION_GROUP
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
    money_group.empty()
    
    DATA = []
    for row in range(ROWS):
        r = [-1] * COLS 
        DATA.append(r)

    return DATA

################################################## JSON File #########################################################

variables = {
    "PLAYER_TYPE" : "Cyborg",
    "High Score" : 0,
    "Level" : 0
}



def write_json(dik = variables):
    json_obj = json.dumps(dik, indent=4)
    with open("local_variable.json", "w") as outfile:
        outfile.write(json_obj)


################################################## Player Action #####################################################
moving_left = moving_right = shoot = grenade = False
grenade_thrown = False 

############################################# Instances  #############################################################

bg = Background(screen=screen)
world = World()
WORLD_DATA = world.get_world_data(0)
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

CUSTOM_GLITCH = {
    'teleport' : False,
    'wallbang' : False
}

glitch_happening = "No Glitch"
glitch_counter = 0

PRESSED_GLITCHED_BUTTON = {
    'teleport' : False,
    'wallbang' : False
}
custom_glitch = "NO GLITCH"
CUSTOM_GLITCH_TIMER = 0
TELEPORT_NUM = 3


######### LEVEL TIMER #################################################
GLITCH_CLOCK = 420

############################### GAME TEMPORARY LAYOUTS ##########################################
SHOW_COLLECT_MONEY = False 

run = True 
while run:
    # Settings
    clock.tick(FPS)


    if game_start == False and not how_to_Scene and not play:
        action = scene.home_screen()
        if action == 1:
            game_start = True 
        elif action == 2:
            run = False 
        elif action == 3:
            how_to_Scene = True 
    
    if how_to_Scene and not game_start and not play:
        action = scene.how_to_play()
        if action == 1:
            game_start = False 
            Level_Select = False 
            how_to_Scene = False 




    if game_start and not play and not how_to_Scene:
        level = scene.select_level()
        if level:
            play = True 
            game_start = False 
            how_to_Scene = False


            ### NEW LEVEL ####
            LEVEL += 0

            variables['Level'] = LEVEL
            write_json(variables)

            BG_SCROLL = 0
            world_data = reset_level()
            if LEVEL <= MAX_LEVELS:
                with open(f'./Levels/level{LEVEL}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                    world = World()
                    player, healthbar = world.process_delta(world_data)
            else:
                pass # ALl Level Complete
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

            PRESSED_GLITCHED_BUTTON = {
                'teleport' : False,
                'wallbang' : False
            }
            custom_glitch = "NO GLITCH"
            CUSTOM_GLITCH_TIMER = 0
            CUSTOM_GLITCH = {
                'teleport' : False,
                'wallbang' : False
            }

            player.score += player.level_score
            TELEPORT_NUM = 3
            ### NEW LEVEL ### 

         

    if play and not how_to_Scene and not game_start:
        #Background
        bg.draw_img_bg(bg_image, BG_SCROLL)

        world.draw(SCREEN_SCROLL)
        
        ############################# UI ########################################################################
        healthbar.draw_player(player.health, screen)
        # Text
        scene.health_and_other_sheets(player)
        # draw_text(f"Ammo: {player.ammo}", FONT, RED, 100, 35)
        # draw_text(f"Grenades: {player.grenades}", FONT, RED, 100,55)
        # draw_text(f"Health: {player.health}", FONT, RED, 100, 75)

        # Visualizing ammo and grenades

        # for i in range(player.grenades):
        #     screen.blit(grenade_img, (135 + (i*20), 40))


        # Items Update
        item_box_group.update(player, SCREEN_SCROLL)
        item_box_group.draw(screen)

        water_group.update(SCREEN_SCROLL)
        water_group.draw(screen)

        exit_group.update(SCREEN_SCROLL)
        exit_group.draw(screen)

        decoration_group.update(SCREEN_SCROLL)
        decoration_group.draw(screen)

        money_group.update(SCREEN_SCROLL, player)
        money_group.draw(screen)
       

        #Enemy
        for enemy in enemy_group:
            healthbar.draw_enemy(enemy.health, screen, enemy)
            bullet = enemy.ai(player, world, SCREEN_SCROLL, BG_SCROLL, water_group, exit_group, GLITCH_LIST['control_glitch'], GLITCH_LIST['direction_glitch'], GLITCH_LIST['gravity_glitch'], CUSTOM_GLITCH['teleport'])
            if bullet:
                bullet_group.add(bullet)
            enemy.draw(screen)
            enemy.update()


        #Player
        player.draw(screen)
        player.update()

        #Bullet
        bullet_group.update(player, enemy_group, bullet_group, world, SCREEN_SCROLL, CUSTOM_GLITCH['wallbang'])
        bullet_group.draw(screen)
    

        #Grenade
        
        grenade_group.update(player, enemy_group, world, SCREEN_SCROLL, GLITCH_LIST['direction_glitch'])
        grenade_group.draw(screen)
        

        #Animation
       
        explosion_group.update(SCREEN_SCROLL)
        explosion_group.draw(screen)

    
    ########################## GLITCH VALUES ####################################
        glitch_types = list(GLITCH_LIST.keys())
       
    
    #################### CONTROLLING GLITCH ########################################
       
        next_glitch = glitch_types[glitch_counter]
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
            GLITCH_CLOCK = 7*FPS #TASK: eta ke random korte hobe 
            
        GLITCH_CLOCK -= 1

        ################# GLITCH BUTTON ##############################################
       

        # scene.ingame_ui(GLITCH_CLOCK // FPS, glitch_happening, next_glitch)
        scene.glitch_ui(GLITCH_LIST['control_glitch'], GLITCH_LIST['direction_glitch'], GLITCH_LIST['gravity_glitch'], GLITCH_CLOCK, next_glitch)
        glitch_action = scene.custom_glitch_ui(custom_glitch, CUSTOM_GLITCH_TIMER // FPS, PRESSED_GLITCHED_BUTTON['teleport'], PRESSED_GLITCHED_BUTTON['wallbang'], TELEPORT_NUM)

        scene.score_ui(player.level_score, player.score, SHOW_COLLECT_MONEY)

        if glitch_action == 1 and CUSTOM_GLITCH_TIMER<=0:
            TELEPORT_NUM -= 1
            CUSTOM_GLITCH['teleport'] = True
            if TELEPORT_NUM<=0:
                PRESSED_GLITCHED_BUTTON['teleport'] = True 
            CUSTOM_GLITCH['wallbang'] = False  
            custom_glitch = "TELEPORT"
            CUSTOM_GLITCH_TIMER = 5*FPS
           
        elif glitch_action == 2 and CUSTOM_GLITCH_TIMER<=0:
            CUSTOM_GLITCH['wallbang'] = True 
            PRESSED_GLITCHED_BUTTON['wallbang'] = True 
            CUSTOM_GLITCH['teleport'] = False  
            custom_glitch = "WALL-BANG"
            CUSTOM_GLITCH_TIMER = 8*FPS
        
        if CUSTOM_GLITCH_TIMER == 0:
            CUSTOM_GLITCH['teleport'] = False
            CUSTOM_GLITCH['wallbang'] = False
            custom_glitch = "NO GLITCH"

        if CUSTOM_GLITCH_TIMER>0:
            CUSTOM_GLITCH_TIMER -= 1
        
        if pygame.sprite.spritecollide(player, exit_group, False) and player.level_score < NEXT_LEVEL_PASS:
            SHOW_COLLECT_MONEY = True 
        else:
            SHOW_COLLECT_MONEY = False 


        
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

            SCREEN_SCROLL, level_complete = player.move(moving_left, moving_right, world, BG_SCROLL, water_group, exit_group, GLITCH_LIST['control_glitch'], GLITCH_LIST['gravity_glitch'], CUSTOM_GLITCH['teleport'])
            BG_SCROLL -= SCREEN_SCROLL

            if level_complete:
                ### NEW LEVEL ####
                LEVEL += 1

                variables['Level'] = LEVEL
                write_json(variables)

                BG_SCROLL = 0
                world_data = reset_level()
                if LEVEL <= MAX_LEVELS:
                    with open(f'./Levels/level{LEVEL}_data.csv', newline='') as csvfile:
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

                PRESSED_GLITCHED_BUTTON = {
                    'teleport' : False,
                    'wallbang' : False
                }
                custom_glitch = "NO GLITCH"
                CUSTOM_GLITCH_TIMER = 0
                CUSTOM_GLITCH = {
                    'teleport' : False,
                    'wallbang' : False
                }

                player.score += player.level_score
                TELEPORT_NUM = 3
                ### NEW LEVEL ###
                

        else:
            action = scene.restart_screen()
            if action == 1:
                BG_SCROLL = 0
                world_data = reset_level()

                with open(f'./Levels/level{LEVEL}_data.csv', newline='') as csvfile:
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
                
                PRESSED_GLITCHED_BUTTON = {
                    'teleport' : False,
                    'wallbang' : False
                }
                custom_glitch = "NO GLITCH"
                CUSTOM_GLITCH_TIMER = 0
                CUSTOM_GLITCH = {
                    'teleport' : False,
                    'wallbang' : False
                }

                player.level_score = 0
                TELEPORT_NUM = 3
                
                            

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