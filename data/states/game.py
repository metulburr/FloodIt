

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
        self.chosen_color = None
        self.user_blocks = []
        self.turns = 0
        self.number_of_blocks_wide = 14
        self.number_of_blocks_high = 14
        self.block_offsetY = 25
        self.block_offsetX = 25
        self.block_bufferX = 135
        self.block_bufferY = 12
        self.max_turns = 25
        self.table = []
        self.games_won = 0
        self.games_lost = 0
        self.update_label()
        self.lost_game = False
        self.take_turn = True

        self.overlay = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay.fill(0)
        self.overlay.set_alpha(200)
        

        
    def update_label(self):
        text = "Turns: {} / {}".format(self.turns, self.max_turns)
        self.turns_text, self.turns_rect = self.make_text(text, (0,0,0), (60, 125), 20)
        
        msg = 'Game Over'
        if self.won_game():
            msg = 'You Won'
        self.game_over, self.game_over_rect = self.make_text(msg, (255,255,255), self.screen_rect.center, 50)
        
        self.games_won_text, self.games_won_rect = self.make_text('Won: {}'.format(self.games_won), (0,0,0), (60, 150), 20)
        self.games_lost_text, self.games_lost_rect = self.make_text('Lost: {}'.format(self.games_lost), (0,0,0), (60, 175), 20)
        
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
        self.cheat_button = button.Button((10,300,105,25),(0,0,100), 
            self.cheat, text='Cheat', clicked_color=(255,255,255), 
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
            self.yellow_button,self.pink_button, self.purple_button, #self.cheat_button
        ]
        
    def cheat(self):
        color = random.choice(self.color_options)
        
        for row in self.table:
            for block in row:
                block.color = color
        while True:
            c = random.choice(self.color_options)
            if c != color:
                break
        self.table[self.number_of_blocks_wide-1][self.number_of_blocks_high-1].color = c
        self.current_color = color
        
    def set_color(self, color):
        self.button_click.sound.play()
        self.turns += 1
        if self.turns == self.max_turns: #game over
            self.chosen_color = color
            self.lost_game = True
            self.turns = self.max_turns
            for button in self.buttons:
                button.disabled = True
        else:
            self.chosen_color = color
    
    def create_table(self):
        self.table = []
        for i in range(self.number_of_blocks_wide):
            row = []
            for j in range(self.number_of_blocks_high):
                row.append(block.Block(self.color_options, (i*self.block_offsetX+self.block_bufferX, j*self.block_offsetY+self.block_bufferY)))
            self.table.append(row)
                
    def flood(self, old_color, new_color, x, y):
        if old_color == new_color or self.table[x][y].color != old_color:
            return
        self.table[x][y].color = new_color
        self.current_color = new_color
        if x > 0:
            self.flood(old_color, new_color, x-1, y)
        if x < self.number_of_blocks_high -1:
            self.flood(old_color, new_color, x+1, y)
        if y > 0:
            self.flood(old_color, new_color, x, y-1)
        if y < self.number_of_blocks_wide - 1:
            self.flood(old_color, new_color, x, y+1)
            
    def won_game(self):
        for row in self.table:
            for block in row:
                if block.color != self.current_color:
                    return False
        return True
        
    def reset_game(self, button_sound=True, counter=True):
        if counter:
            if self.lost_game:
                self.games_lost += 1
            if self.won_game():
                self.games_won += 1
            self.write_save()
            
        self.lost_game = False
        self.turns = 0
        self.create_table()
        self.user_blocks = []
        self.user_blocks.append(self.table[0][0])
        self.current_color = self.table[0][0].start_color
        for button in self.buttons:
            button.disabled = False
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
            if not button.disabled:
                button.check_event(event)
        self.menu_button.check_event(event)
                    
    def update(self, now, keys):
        self.update_label()
        self.flood(self.current_color, self.chosen_color, 0,0)
        #self.table[0][0].color = pg.Color('black')
        for row in self.table:
            for block in row:
                block.update()
        if self.won_game():
            for button in self.buttons:
                button.disabled = True
        if self.lost_game:
            pass
        
    def render(self, screen):
        screen.fill((self.bg_color))
        for button in self.buttons:
            button.render(screen)
        for row in self.table:
            for block in row:
                block.render(screen)
        screen.blit(self.turns_text, self.turns_rect)
        screen.blit(self.games_won_text, self.games_won_rect)
        screen.blit(self.games_lost_text, self.games_lost_rect)
        if self.lost_game or self.won_game():
            screen.blit(self.overlay, (0,0))
            screen.blit(self.game_over, self.game_over_rect)
        self.menu_button.render(screen)


    def load_save(self):
        #won / loss / points
        path = os.path.join('data', 'save.txt')
        with open(path) as f:
            data = f.read()
        self.games_won = int(data.split()[0])
        self.games_lost = int(data.split()[1])
        #self.points = int(data.split()[2])
        
    def write_save(self):
        #won / loss / points
        path = os.path.join('data', 'save.txt')
        with open(path, 'w') as f:
            f.write(str(self.games_won) + '\n' + str(self.games_lost))
        
    def cleanup(self):
        pass
        
    def entry(self):
        self.reset_game(button_sound=False, counter=False)
        self.load_save()
