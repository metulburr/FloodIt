
import os
import pygame as pg
from .states import menu, splash, title, game, options
from data.tools import DB

class Control():
    def __init__(self, **settings):
        self.__dict__.update(settings)
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        self.monitor = (pg.display.Info().current_w, pg.display.Info().current_h)
        pg.display.set_caption(self.caption)
        self.default_screensize = (int(self.size[0]), int(self.size[1]))
        self.screensize = (int(self.size[0]), int(self.size[1]))
        if self.fullscreen:
            self.screen = pg.display.set_mode(self.screensize, pg.FULLSCREEN)
        else:
            if self.resizable:
                self.screen = pg.display.set_mode(self.screensize, pg.RESIZABLE)
            else:
                os.environ["SDL_VIDEO_CENTERED"] = "True"
                self.screen = pg.display.set_mode(self.screensize)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.done = False
        self.state_dict = {
            "MENU"     : menu.Menu(self.screen_rect),
            "SPLASH"   : splash.Splash(self.screen_rect),
            'TITLE'    : title.Title(self.screen_rect),
            'GAME'     : game.Game(self.screen_rect),
            'OPTIONS'  : options.Options(self.screen_rect, self.default_screensize, self.fullscreen),
        }

        self.state_name = "SPLASH"
        self.state = self.state_dict[self.state_name]
            
    def check_display_change(self):
        if self.state.change_res:
            pg.display.quit()
            pg.display.init()
            if self.state.change_res == 'fullscreen':
                if not self.fullscreen:
                    self.screen = pg.display.set_mode(self.screensize, pg.FULLSCREEN)
                else:
                    os.environ["SDL_VIDEO_CENTERED"] = "True"
                    self.screen = pg.display.set_mode(self.screensize)
                self.fullscreen = not self.fullscreen
                self.screen_rect = self.screen.get_rect()
            else:
                self.fullscreen = False
                self.screen = pg.display.set_mode(self.state.change_res)
                self.screen_rect = self.screen.get_rect()
            self.state.change_res = None
            self.save_settings()
            self.state.setup_buttons() #options state only method (update buttons status)
            
    def save_settings(self):
        s = {
            'fullscreen':self.fullscreen,
            'difficulty':self.difficulty,
            'size'      :self.screen_rect.size,
            'caption'   :self.caption,
            'resizable' :self.resizable,
        }
        
        DB.save('settings', s)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type in (pg.KEYDOWN,pg.KEYUP):
                self.keys = pg.key.get_pressed()
                

            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                self.screen_rect = self.screen.get_rect()
            self.state.get_event(event, self.keys)

    def change_state(self):
        if self.state.done:
            self.state.cleanup()
            self.state_name = self.state.next
            self.state.done = False
            self.state = self.state_dict[self.state_name]
            self.state.entry()


    def run(self):
        while not self.done:
            if self.state.quit:
                self.done = True
            self.check_display_change()
            now = pg.time.get_ticks()
            self.event_loop()
            self.change_state()
            self.state.update(now, self.keys)
            self.state.render(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


