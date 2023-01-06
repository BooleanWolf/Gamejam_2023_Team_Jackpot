import pygame
from Settings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def transform_image(img, scale):
    return pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))

def flip_image_y(img):
    return pygame.transform.flip(img, False, True)

def flip_image_x(img):
    return pygame.transform.flip(img, True, False)



############################### Loading Images #####################################
bullet_img = pygame.image.load("./assets/Weapons/Bullets/Laser_borg.png").convert_alpha()
bullet_img = transform_image(bullet_img, 0.2)

grenade_img = pygame.image.load('./assets/Weapons/Grenades/0.png').convert_alpha()

health_box = pygame.image.load('./assets/ItemBox/health_box.png').convert_alpha()
ammo_box = pygame.image.load('./assets/ItemBox/ammo_box.png').convert_alpha()
grenade_box = pygame.image.load('./assets/ItemBox/grenade_box.png').convert_alpha()
money_box = pygame.image.load('./assets/Animated _Jinish/Money/0.PNG').convert_alpha()

# Tiles 
TILES_IMG_LIST = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'./assets/TILES/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    TILES_IMG_LIST.append(img)

####### Background Image ###########
bg_image = pygame.image.load('./assets/Background/wallpaper.jpg')
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_image.set_alpha(128)

homeScreen_img = pygame.image.load('./assets/HomeScreen/HomeScreen.png')
homeScreen_img = pygame.transform.scale(homeScreen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

playButton_img = pygame.image.load('./assets/Buttons/play_button.png').convert_alpha()
exitbtn_img = pygame.image.load('./assets/Buttons/exit_btn.png').convert_alpha()
restartbtn_img = pygame.image.load('./assets/Buttons/restart_btn.png').convert_alpha()

control_glitch_btn_img=  pygame.image.load('./assets/Buttons/control_glitch_btn.png').convert_alpha()

######################### UI ##################################################
controlG_img = pygame.image.load('./assets/UI/Control_ON.png').convert_alpha()
controlG_img = transform_image(controlG_img, 0.8)
directionG_img = pygame.image.load('./assets/UI/Direction_ON.png').convert_alpha()
directionG_img = transform_image(directionG_img, 0.8)
gravityG_img = pygame.image.load('./assets/UI/Gravity_ON.png').convert_alpha()
gravityG_img = transform_image(gravityG_img, 0.8)

teleport_btn_img = pygame.image.load('./assets/Buttons/teleport_glitch_btn.png').convert_alpha()


wallbang_btn_img = pygame.image.load('./assets/Buttons/wallbang_glitch_btn.png').convert_alpha()

custom_timer = pygame.image.load('./assets/UI/custom_timer.png').convert_alpha()
custom_timer = transform_image(custom_timer, 0.4)

how_to_scene = pygame.image.load('./assets/Scenes/How_to_play.png').convert_alpha()
how_to_scene = pygame.transform.scale(how_to_scene, (SCREEN_WIDTH, SCREEN_HEIGHT))

gravity_in = pygame.image.load('./assets/Buttons/gravity_in.png').convert_alpha()
direct_in = pygame.image.load('./assets/Buttons/direct_in.png').convert_alpha()
control_in =  pygame.image.load('./assets/Buttons/contol_in.png').convert_alpha()

gravity_in = transform_image(gravity_in, 0.8)
direct_in = transform_image(direct_in, 0.8)
control_in = transform_image(control_in, 0.8)

how_to_btn = pygame.image.load('./assets/Buttons/how_to_btn.png').convert_alpha()

back_btn = pygame.image.load('./assets/Buttons/back_btn.png').convert_alpha()

##################################### LEVEL SELECT ################################################

level_btns = []

for i in range(1, 26):
    level0_btn = pygame.image.load(f'./assets/LevelSelectScene/{i}.jpeg').convert_alpha()
    level0_btn = pygame.transform.scale(level0_btn, (300, 300))
    level_btns.append(level0_btn)