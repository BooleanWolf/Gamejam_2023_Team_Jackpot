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