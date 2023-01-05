import pygame 
from ImageGraphics import *
from Graphics import *

play_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2  -100, playButton_img, 0.3)
exit_btn = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, exitbtn_img, 0.3)
restart_btn = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, restartbtn_img, 1)

class Scene:
    def __init__(self, screen) -> None:
        self.screen = screen
    
    def home_screen(self):
        self.screen.blit(homeScreen_img, (0, 0))
        if play_button.draw(self.screen):
            return 1 
        if exit_btn.draw(self.screen):
            return 2
    
    def restart_screen(self):
        if restart_btn.draw(self.screen):
            return 1
        

