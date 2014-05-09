

import pygame as pg
from .. import tools
from ..toolbox import button, roundrects
import random

class Menu(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.options = ['Play', 'Quit']
        self.next_list = ['GAME']
        self.pre_render_options()
        self.from_bottom = 300
        self.spacer = 35

        self.bg_orig = tools.Image.load('bg.png')
        self.bg = pg.transform.scale(self.bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        
        self.menu_item_bg_w = 200
        self.menu_item_bg_h = 25

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
                roundrects.round_rect(screen, (aligned_center[0]-(w//2), aligned_center[1]-(h//2),w,h), (0,0,0), 5, 2, (50,50,50))
            opt[1].center =  aligned_center
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                rect = opt[1]
                screen.blit(opt[0],rect)
        
        
    def cleanup(self):
        pass
        
    def entry(self):
        pass

