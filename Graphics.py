import pygame

SCREEN_WIDTH = 1600
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
        pygame.draw.line(self.screen, RED, (0, 400), (SCREEN_WIDTH, 400))

    
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
