
import random
import pygame as pg

class Block:
    def __init__(self, options, topleft_):
        self.size = 25
        self.start_color = random.choice(options)
        self.image = pg.Surface([self.size, self.size]).convert()
        self.image.fill(self.start_color)
        self.rect = self.image.get_rect(topleft=topleft_)
        
    def fill(self, color):
        self.image.fill(color)
    
    def render(self, screen):
        screen.blit(self.image, self.rect)
