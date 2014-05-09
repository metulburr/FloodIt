
import pygame as pg
from .. import tools

class Title(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.next = "MENU"
        self.timeout = 10
        self.start_time = 0

        self.cover = pg.Surface((screen_rect.width, screen_rect.height))
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step = 3

        self.image_orig = tools.Image.load('bg.png')
        self.image = pg.transform.scale(self.image_orig, (self.screen_rect.width, self.screen_rect.height))
        text = ['Press Any Key']
        self.rendered_text = self.make_text_list("Fixedsys500c",25,text,(255,255,255),400,50)
        
        self.blink = False
        self.blink_time = 1.0
        self.blink_timer = 0

    def make_text_list(self,font,size,strings,color,start_y,y_space):
        rendered_text = []
        for i,string in enumerate(strings):
            msg = self.render_font(font,size,string,color)
            rect = msg.get_rect(center=(self.screen_rect.centerx,start_y+i*y_space))
            rendered_text.append((msg,rect))
        return rendered_text

    def render_font(self,font,size,msg,color=(255,255,255)):
        selected_font = tools.Font.load('impact.ttf', size)
        return selected_font.render(msg,1,color)

    def update(self,surface,keys):
        self.current_time = pg.time.get_ticks()
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        if self.current_time-self.start_time > 1000.0*self.timeout:
            self.done = True
        elif self.current_time-self.blink_timer > 1000/self.blink_time:
            self.blink = not self.blink
            self.blink_timer = self.current_time
            
    def render(self, screen):
        #screen.blit(self.image, (0,0))
        screen.blit(self.cover,(0,0))
        if self.blink:
            for msg in self.rendered_text:
                screen.blit(*msg)

    def get_event(self,event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            self.done = True
            
    def cleanup(self):
        pass
        
    def entry(self):
        pass
