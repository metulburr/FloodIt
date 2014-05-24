

import pygame as pg
import os
import shutil
import random
import sys
import json
        
class DB:
    dirname = 'save'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    path = os.path.join(dirname, 'database{}'.format(sys.version.split()[0]))
    #key = 'database'
    @staticmethod
    def exists():
        return os.path.exists(DB.path)
    @staticmethod
    def load():
        data = open(DB.path)
        obj = json.load(data)
        data.close()
        return obj
    @staticmethod
    def save(obj):
        f = open(DB.path, 'w')
        f.write(json.dumps(obj))
        f.close()
    
        
class Image:
    path = os.path.join('resources', 'graphics')
    @staticmethod
    def load(filename):
        p = os.path.join(Image.path, filename)
        return pg.image.load(os.path.abspath(p))

class Font:
    path = os.path.join('resources', 'fonts')
    @staticmethod
    def load(filename, size):
        p = os.path.join(Font.path, filename)
        return pg.font.Font(os.path.abspath(p), size)

class Sound:
    path = os.path.join('resources', 'sound')
    def __init__(self, filename):
        self.fullpath = os.path.join(Sound.path, filename)
        pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=128)
        self.sound = pg.mixer.Sound(self.fullpath)
        
class Music:
    def __init__(self, volume, song=None):
        self.path = os.path.join('resources', 'music')
        self.volume = volume
        self.song = song
        self.track_end = pg.USEREVENT+1
        self.tracks = []
        self.track = 0
        
    def load_list(self, file_list):
        for track in file_list:
            self.tracks.append(os.path.join(self.path, track))
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.set_endevent(self.track_end)
        pg.mixer.music.load(self.tracks[0])
        
    def load_single(self):
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.set_endevent(self.track_end)
        pg.mixer.music.load(os.path.join(self.path, self.song))

class States:
    def __init__(self):     
        self.change_res = None  
        self.res = None
        self.sound = True
        self.music = True
        self.change_sound = None
        
        self.bogus_rect = pg.Surface([0,0]).get_rect()
        self.screen_rect = self.bogus_rect
        self.button_volume = .2
        self.button_hover_volume = .1
        self.button_click = Sound('button.wav')
        self.button_click.sound.set_volume(self.button_volume)
        self.button_hover = Sound('button_hover.wav')
        self.button_hover.sound.set_volume(self.button_hover_volume)
        self.background_music_volume = .3
        #self.background_music = Music(self.background_music_volume)
        self.background_music = None
        self.bg_color = (25,25,25)
        self.timer = 0.0
        self.quit = False
        self.done = False
        self.rendered = None
        self.next_list = None
        self.last_option = None
        self.gametitle = 'Boom'
        
        self.menu_option_deselect_color = (105,95,0)
        self.menu_option_select_color = (255,255,255)
        self.title_color = (50,50,50)
        self.text_basic_color = (255,255,255)
        self.text_hover_color = (100,100,100)
        self.text_color = self.text_basic_color 
        
        
        self.selected_index = 0
        
        self.action = None
        self.keybinding = {
            'up'    : [pg.K_UP, pg.K_w],
            'down'  : [pg.K_DOWN, pg.K_s],
            'right' : [pg.K_RIGHT, pg.K_d],
            'left'  : [pg.K_LEFT, pg.K_a],
            'select': pg.K_RETURN, 
            'pause' : pg.K_p,
            'back'  : pg.K_ESCAPE
        }
        
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.yellow = (255,255,0)
        self.pink = (225,125,225)
        self.purple = (140,0,140)
        
        self.color_options = [
            self.blue, self.red, self.green, self.yellow, self.pink, self.purple
        ]
        
    def update_controller_dict(self, keyname, event):
        self.controller_dict[keyname] = event.key
        
    def mouse_hover_sound(self):
        for i,opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                if self.last_option != opt:
                    if self.sound:
                        self.button_hover.sound.play()
                    self.last_option = opt
                    
    def mouse_menu_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i,opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break
                    
    def make_text(self,message,color,center,size, fonttype='impact.ttf'):
        font = Font.load(fonttype, size)
        text = font.render(message,True,color)
        rect = text.get_rect(center=center)
        return text,rect
        
    def pre_render_options(self):
        font_deselect = Font.load('impact.ttf', 20)
        font_selected = Font.load('impact.ttf', 20)

        rendered_msg = {"des":[],"sel":[], 'bg':[]}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, self.menu_option_deselect_color)
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, self.menu_option_select_color)
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend,d_rect))
            rendered_msg["sel"].append((s_rend,s_rect))
        self.rendered = rendered_msg
        
    def select_option(self, i):
        '''select menu option via keys or mouse'''
        if i == len(self.next_list):
            self.quit = True
        else:
            if self.sound:
                self.button_click.sound.play()
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, op=0):
        '''change highlighted menu option'''
        for i,opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i

        if op:
            self.selected_index += op
            max_ind = len(self.rendered['des'])-1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0
            if self.sound:
                self.button_hover.sound.play()

def clean_files():
    '''remove all pyc files and __pycache__ direcetories in subdirectory'''
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                path = os.path.join(root, dir)
                print('removing {}'.format(os.path.abspath(path)))
                shutil.rmtree(path)
        for name in files:
            if name.endswith('.pyc'):
                path = os.path.join(root, name)
                print('removing {}'.format(os.path.abspath(path)))
                os.remove(path)


class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pg.Surface(rect.size).convert()
    #surface.fill(0)
    #surface.set_alpha(0)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface
    
    
