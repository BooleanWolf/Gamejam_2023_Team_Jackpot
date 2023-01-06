import pygame 
from ImageGraphics import *
from Graphics import *

play_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2  -100, playButton_img, 0.3)
exit_btn = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, exitbtn_img, 0.3)
restart_btn = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, restartbtn_img, 1)
controlGlitch_btn = Button(200, 20, control_glitch_btn_img, 0.2)
class Scene:
    def __init__(self, screen) -> None:
        self.screen = screen
    
    def draw_text(self, string, coordx, coordy, fontSize):
        font = pygame.font.SysFont('Comic Sans MS', fontSize)
        text = font.render(string, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (coordx, coordy) 
        return (text, textRect)

    
    def home_screen(self):
        self.screen.blit(homeScreen_img, (0, 0))
        if play_button.draw(self.screen):
            return 1 
        if exit_btn.draw(self.screen):
            return 2
    
    def restart_screen(self):
        if restart_btn.draw(self.screen):
            return 1
    
    def ingame_ui(self, glitch_timer, which_glitch, next_glitch):
        glitch_timer_text = self.draw_text(f"GLITCH: {glitch_timer}", 750, 40, 30)
        self.screen.blit(glitch_timer_text[0], glitch_timer_text[1])

        which_glitch_text = self.draw_text(f"{which_glitch}", 950, 40, 30)
        self.screen.blit(which_glitch_text[0], which_glitch_text[1])

        next_glitch_text = self.draw_text(f"Next Glitch: {next_glitch}", 950, 70, 30)
        self.screen.blit(next_glitch_text[0], next_glitch_text[1])
    
    def ingame_ui_for_custom(self, custom_glitch, custom_glitch_timer, tp, wb):
        custom_glitch_txt = self.draw_text(f"Active Glitch: {custom_glitch} Time: {custom_glitch_timer}", 950, 100, 30)
        self.screen.blit(custom_glitch_txt[0], custom_glitch_txt[1])
        # if not tp:
        #     if controlGlitch_btn.draw(self.screen):
        #         return 1
        if not wb:
            if controlGlitch_btn.draw(self.screen):
                return 2
       
        
        
        

