import pygame
from pygame import mixer


mixer.init()
pygame.init()

pygame.mixer.music.load('./assets/Audio/bg_music.mp3')
pygame.mixer.music.set_volume(0.2)

jump_fx = pygame.mixer.Sound('./assets/Audio/jump.wav')
jump_fx.set_volume(0.7)
shot_fx = pygame.mixer.Sound('./assets/Audio/shot.mp3')
shot_fx.set_volume(0.3)
grenade_fx = pygame.mixer.Sound('./assets/Audio/grenade.wav')
grenade_fx.set_volume(0.4)
glitch_change = pygame.mixer.Sound('./assets/Audio/Glitch_change.mp3')
glitch_change.set_volume(0.6)
custom_glitch_music = pygame.mixer.Sound('./assets/Audio/Custom_Glitch.mp3')
custom_glitch_music.set_volume(0.6)
level_change_music = pygame.mixer.Sound('./assets/Audio/level_change.mp3')
level_change_music.set_volume(0.4)
getting_hit_fx = pygame.mixer.Sound('./assets/Audio/getting_hit.mp3')
getting_hit_fx.set_volume(0.3)