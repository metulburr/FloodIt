

import pygame as pg
from .. import tools
from ..toolbox import button
from ..components import block
import os
import random

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.overlay_bg = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay_bg.fill(0)
        self.overlay_bg.set_alpha(200)
        self.overlay_card_position = (100,200)
        self.bg_color = (255,255,255)
        self.setup_btns()
        self.current_color = None
        self.next_color = None
        self.turns = 0
        self.max_turns = 25
        self.update_label()
        self.in_game = True
        self.block_bufferX = 135
        self.block_bufferY = 12
        
        self.overlay = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay.fill(0)
        self.overlay.set_alpha(200)
        
    def update_label(self):
        text = "Turns: {} / {}".format(self.turns, self.max_turns)
        self.turns_text, self.turns_rect = self.make_text(text, (0,0,0), (60, 125), 20)
        
        self.game_over, self.game_over_rect = self.make_text('Game Over', (255,255,255), self.screen_rect.center, 50)
        
    def setup_btns(self):
        self.buttons = []
        
        button_config = {
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (205,195, 0),
            'font'               : tools.Font.load('impact.ttf', 18),
            'font_color'         : (255,255,255),
            'border_color'       : (0,0,0),
        }
        c = (0,0,0) #clicked color for color buttons
        self.menu_button = button.Button((10,10,105,25),(0,0,100), 
            self.reset_game, text='New Game', clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        self.blue_button = button.Button((10,45,25,25),self.blue, 
            lambda:self.set_color(self.blue), clicked_color=c,  hover_color=(0,0,200), **button_config
        )
        self.red_button = button.Button((50,45,25,25),self.red, 
            lambda:self.set_color(self.red), clicked_color=c,  hover_color=(200,0,0), **button_config
        )
        self.green_button = button.Button((90,45,25,25),self.green, 
            lambda:self.set_color(self.green), clicked_color=c,  hover_color=(0,200,0), **button_config
        )
        self.yellow_button = button.Button((10,80,25,25),self.yellow, 
            lambda:self.set_color(self.yellow), clicked_color=c,  hover_color=(200,200,0), **button_config
        )
        self.pink_button = button.Button((50,80,25,25),self.pink, 
            lambda:self.set_color(self.pink), clicked_color=c,  hover_color=(170,70,170), **button_config
        )
        self.purple_button = button.Button((90,80,25,25),self.purple, 
            lambda:self.set_color(self.purple), clicked_color=c,  hover_color=(170,70,95), **button_config
        )
        self.buttons += [
            self.blue_button, self.red_button, self.green_button,
            self.yellow_button,self.pink_button, self.purple_button
        ]
        
    def set_color(self, color):
        self.button_click.sound.play()
        self.turns += 1
        if self.turns == self.max_turns +1: #game over
            self.in_game = False
            self.turns = self.max_turns
        else:
            self.next_color = color
    
    def create_table(self):
        self.table = []
        for i in range(14):
            for j in range(14):
                self.table.append(block.Block(self.color_options, (i*25+self.block_bufferX,j*25+self.block_bufferY)))

    def reset_game(self, button_sound=True):
        self.in_game = True
        self.turns = 0
        self.create_table()
        if button_sound:
            self.button_click.sound.play()
        
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                self.button_click.sound.play()
                self.done = True
                self.next = 'MENU'
                
        #elif event.type == self.bg_music.track_end:
        #    self.bg_music.track = (self.bg_music.track+1) % len(self.bg_music.tracks)
        #    pg.mixer.music.load(self.bg_music.tracks[self.bg_music.track]) 
        #    pg.mixer.music.play()
        for button in self.buttons:
            button.check_event(event)
        self.menu_button.check_event(event)
                    
    def update(self, now, keys):
        self.update_label()
        
    def render(self, screen):
        screen.fill((self.bg_color))
        for button in self.buttons:
            button.render(screen)
        for block in self.table:
            block.render(screen)
        screen.blit(self.turns_text, self.turns_rect)
        if not self.in_game:
            screen.blit(self.overlay, (0,0))
            screen.blit(self.game_over, self.game_over_rect)
        self.menu_button.render(screen)
            
    def cleanup(self):
        pass
        
    def entry(self):
        self.reset_game(button_sound=False)
