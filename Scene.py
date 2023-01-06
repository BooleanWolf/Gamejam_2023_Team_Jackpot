import pygame 
from ImageGraphics import *
from Graphics import *
import os
import math

play_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2  -100, playButton_img, 0.3)
exit_btn = Button(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 280, exitbtn_img, 0.4)
restart_btn = Button(SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 - 60, restartbtn_img, 0.6)
controlGlitch_btn = Button(200, 20, control_glitch_btn_img, 0.2)

teleport_btn = Button(SCREEN_WIDTH - 70, 20, teleport_btn_img, 0.5)
wallbang_btn = Button(SCREEN_WIDTH - 70, 90, wallbang_btn_img, 0.5)

how_to = Button(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 200, how_to_btn, 0.4)

backBtn = Button(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 80, back_btn, 0.3)


######### LEVEL BUTTONS #####################################################################

# for i in range(0, 7):
#     print(f"level{1+i} = Button({10+150*i}, 10, level_btns[{i}], 0.4)")

# for i in range(7, 15):
#     print(f"level{1+i} = Button({10+150*(i-7)}, 160, level_btns[{i}], 0.4)")

level1 = Button(80, 200, level_btns[0], 0.4)
level2 = Button(230, 200, level_btns[1], 0.4)
level3 = Button(380, 200, level_btns[2], 0.4)
level4 = Button(530, 200, level_btns[3], 0.4)
level5 = Button(680, 200, level_btns[4], 0.4)
level6 = Button(830, 200, level_btns[5], 0.4)
level7 = Button(980, 200, level_btns[6], 0.4)
level8 = Button(10, 450, level_btns[7], 0.4)
level9 = Button(160, 450, level_btns[8], 0.4)
level10 = Button(310, 450, level_btns[9], 0.4)
level11 = Button(460, 450, level_btns[10], 0.4)
level12 = Button(610, 450, level_btns[11], 0.4)
level13 = Button(760, 450, level_btns[12], 0.4)
level14 = Button(910, 450, level_btns[13], 0.4)
level15 = Button(1060, 450, level_btns[14], 0.4)

class Scene:
    def __init__(self, screen) -> None:
        self.screen = screen
    
    def draw_text(self, string, coordx, coordy, fontSize, Color = (0, 0, 0)):
        font = pygame.font.Font(os.path.join("assets", "Fonts", 'Rexlia.otf'), fontSize)
        text = font.render(string, True, Color)
        textRect = text.get_rect()
        textRect.center = (coordx, coordy) 
        return (text, textRect)
    
    def draw_number(self, string, x, y, fontsize, Color = (255, 255, 255)):
        font = pygame.font.Font(os.path.join("assets", "Fonts", 'SGT.ttf'), fontsize)
        text = font.render(string, True, Color)
        textRect = text.get_rect()
        textRect.center = (x, y) 
        return (text, textRect)

    
    def home_screen(self):
        self.screen.blit(homeScreen_img, (0, 0))
        if play_button.draw(self.screen):
            return 1 
        if exit_btn.draw(self.screen):
            return 2
        if how_to.draw(self.screen):
            return 3
    
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
    
    def health_and_other_sheets(self, player):
        heart_img = pygame.image.load('./assets/HomeScreen/HEART.png').convert_alpha()
        bullet_img = pygame.image.load('./assets/HomeScreen/BULLET.png').convert_alpha()

        heart_img = transform_image(heart_img, 0.15)
        self.screen.blit(heart_img, (15, 18))
        bullet_img = transform_image(bullet_img, 0.1)
        self.screen.blit(bullet_img, (15, 50))

        bullet_number = self.draw_number(f"{player.ammo}", 70, 68, 30)
        self.screen.blit( bullet_number[0],  bullet_number[1])

        for i in range(0, player.grenades):
            grg = transform_image(grenade_img, 1.2)
            screen.blit(grg, (15 + (i*20), 102))

    def drawArc(self, color, center, radius, width, end_angle):
        arc_rect = pygame.Rect(0, 0, radius*2, radius*2)
        arc_rect.center = center
        pygame.draw.arc(self.screen, color, arc_rect, 0, end_angle, width)

    def glitch_ui(self, control, direction, gravity, time_left, next_glitch):
        nxtg = ''
        
        if next_glitch == 'gravity_glitch':
            nxtg = "GRAVITY"
        
        if next_glitch == 'direction_glitch':
            nxtg = "GRENADE & BULLET"

        if next_glitch == 'control_glitch':
            nxtg = "CONTROL"

        if control:
            self.screen.blit(controlG_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 145))
            self.screen.blit(control_in, (10, SCREEN_HEIGHT - 3*TILE_SIZE + 10))
        elif direction:
            self.screen.blit(directionG_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 145))
            self.screen.blit(direct_in, (10, SCREEN_HEIGHT - 3*TILE_SIZE + 10))
        elif gravity:
            self.screen.blit(gravityG_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 145))
            self.screen.blit(gravity_in, (10, SCREEN_HEIGHT - 3*TILE_SIZE + 10))
        
        self.drawArc((255, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50), 30, 10, 2*math.pi*(time_left/420))
        timer = self.draw_number(f"{time_left // FPS}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 30)
        self.screen.blit(timer[0], timer[1])
        
        

        nextg = self.draw_text(f"upcoming--{nxtg}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10, 15, (255, 255, 255))
        self.screen.blit(nextg[0], nextg[1])
        
    def custom_glitch_ui(self, custom_glitch, custom_glitch_timer, tp, wb, tp_num):
        if custom_glitch != "NO GLITCH":
            self.screen.blit(custom_timer, (SCREEN_WIDTH - 3*TILE_SIZE, SCREEN_HEIGHT - 3*TILE_SIZE + 20))
            time = self.draw_text(f"{custom_glitch_timer}", SCREEN_WIDTH - 3*TILE_SIZE + 50, SCREEN_HEIGHT - 3*TILE_SIZE + 95, 40, (255,255,255))
            self.screen.blit(time[0], time[1])
            pass
        
        if not tp:
            txt = self.draw_number(f"{tp_num}", SCREEN_WIDTH - 100, 50, 20)
            self.screen.blit(txt[0], txt[1])
            txt1 = self.draw_number(f"Teleport", SCREEN_WIDTH - 100, 65, 10)
            self.screen.blit(txt1[0], txt1[1])
            if teleport_btn.draw(self.screen):
                return 1
        if not wb:
            txt = self.draw_number(f"{1}", SCREEN_WIDTH - 100, 120, 20)
            self.screen.blit(txt[0], txt[1])
            txt1 = self.draw_number(f"WallBang", SCREEN_WIDTH - 100, 135, 10)
            self.screen.blit(txt1[0], txt1[1])
            if wallbang_btn.draw(self.screen):
                return 2
    def score_ui(self, level_score, total_score, show_collect_money):

        if show_collect_money:
            msg = self.draw_text(f"{NEXT_LEVEL_PASS - level_score} more point needed to go the next level!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 30, (255, 255, 255))
            self.screen.blit(msg[0], msg[1])

        self.screen.blit(money_box, (15, 135))
        lvl = self.draw_number(f"{level_score}", 70, 150, 30, (0, 255, 0))
        self.screen.blit(lvl[0], lvl[1])
    
    def how_to_play(self):
        self.screen.blit(how_to_scene, (0, 0))

        if backBtn.draw(self.screen):
            return 1
    
    def select_level(self):
        with open("local_variable.json", "r") as openfile:
            json_obj = json.load(openfile)
            
        last_level = json_obj['Level']
        self.screen.blit(bg_image, (0, 0))

        header = self.draw_text(f"Select a level", SCREEN_WIDTH // 2 - 45, 70, 70, (255,255,255))
        self.screen.blit(header[0], header[1])

        footer = self.draw_text(f"Last Level Played: {last_level}", SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT - 150, 50, (255,255,255))
        self.screen.blit(footer[0], footer[1])

        if level1.draw(self.screen):
            return 1
        if level2.draw(self.screen):
            return 2
        if level3.draw(self.screen):
            return 3
        if level4.draw(self.screen):
            return 4
        if level5.draw(self.screen):
            return 5
        if level6.draw(self.screen):
            return 6
        if level7.draw(self.screen):
            return 7
        if level8.draw(self.screen):
            return 8
        if level9.draw(self.screen):
            return 9
        if level10.draw(self.screen):
            return 10
        if level11.draw(self.screen):
            return 11
        if level12.draw(self.screen):
            return 12
        if level13.draw(self.screen):
            return 13
        if level14.draw(self.screen):
            return 14
        if level15.draw(self.screen):
            return 15

        pass
            

       
        
        
        

