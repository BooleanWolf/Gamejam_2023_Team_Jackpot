import pygame
from ImageGraphics import *


SCREEN_WIDTH = 1200
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont('Futura', 30)


class Background:
    def __init__(self, screen, colour = (144, 201, 120)) -> None:
        self.screen = screen
        self.colour = colour
        pass 

    def draw_simple_bg(self):
        self.screen.fill(self.colour)
    
    def draw_img_bg(self, bg_img, bg_scroll):
        self.screen.fill(self.colour)
        width = bg_img.get_width()
        for i in range(9):
            self.screen.blit(bg_img, (width * i - bg_scroll, 0))
       

    
class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y 
        self.health = health
        self.max_health = max_health 

    def draw_player(self, health, screen):
        self.health = health 
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * (self.health/self.max_health), 20))
    
    def draw_enemy(self, health, screen, enemy):
        self.health = health 
        pygame.draw.rect(screen, BLACK, (enemy.rect.centerx - 20, enemy.rect.centery - 30, 44, 8))
        pygame.draw.rect(screen, RED, (enemy.rect.centerx - 18, enemy.rect.centery - 28, 40, 4))
        pygame.draw.rect(screen, GREEN, (enemy.rect.centerx - 18, enemy.rect.centery - 28, 40 * (self.health/self.max_health), 4))

class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = transform_image(image, scale)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action