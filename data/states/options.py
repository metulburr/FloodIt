

import pygame as pg
from .. import tools
from ..toolbox import button
import random

class Options(tools.States):
    def __init__(self, screen_rect, default):
        tools.States.__init__(self)
        self.default_screensize = default
        self.screen_rect = screen_rect
        self.options = ['Back']
        self.next_list = ['MENU']
        self.pre_render_options()
        self.from_bottom = 300
        self.spacer = 35

        self.bg_orig = tools.Image.load('bg.png')
        self.bg = pg.transform.scale(self.bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        
        self.menu_item_bg_w = 200
        self.menu_item_bg_h = 25
        
        button_config = {
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (205,195, 0),
            'font'               : tools.Font.load('impact.ttf', 18),
            'font_color'         : (255,255,255),
            'border_color'       : (0,0,0),
        }
        c = (0,0,0) #clicked color for color buttons
        self.fullscreen_button = button.Button((10,10,105,25),(0,0,100), 
            self.toggle_fullscreen, text='Fullscreen', clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        self.window_button = button.Button((10,40,105,25),(0,0,100), 
            lambda:self.set_window((800, 600)), text='(800, 600)', clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        self.default_button = button.Button((10,70,105,25),(0,0,100), 
            lambda:self.set_window(self.default_screensize), text=str(self.default_screensize), clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        self.buttons = [self.fullscreen_button, self.window_button, self.default_button]
        
    def toggle_fullscreen(self):
        self.change_res = 'fullscreen'
        
    def set_window(self, newsize):
        self.change_res = newsize

    def render_cursor(self, screen):
        mouseX, mouseY = pg.mouse.get_pos()
        self.cursor_rect = self.cursor.get_rect(center=(mouseX+10, mouseY+13))
        screen.blit(self.cursor, self.cursor_rect)

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
                
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        for button in self.buttons:
            button.check_event(event)
        #elif event.type == self.intro.track_end:
        #    self.intro.track = (self.intro.track+1) % len(self.intro.tracks)
        #    pg.mixer.music.load(self.intro.tracks[self.intro.track]) 

        self.mouse_menu_click(event)

    def update(self, now, keys):
        self.mouse_hover_sound()
        self.change_selected_option()

    def render(self, screen):
        screen.fill((0,0,0))
        #screen.blit(self.bg, self.bg_rect)
        for i,opt in enumerate(self.rendered["des"]):
            aligned_center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            
            for option in self.options:
                w = self.menu_item_bg_w
                h = self.menu_item_bg_h
                #roundrects.round_rect(screen, (aligned_center[0]-(w//2), aligned_center[1]-(h//2),w,h), (0,0,0), 5, 2, (50,50,50))
            opt[1].center =  aligned_center
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                rect = opt[1]
                screen.blit(opt[0],rect)
        for button in self.buttons:
            button.render(screen)
        
        
    def cleanup(self):
        pass
        
    def entry(self):
        pass

