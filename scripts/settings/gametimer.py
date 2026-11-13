from .constants import *
from .imports import pygame

class GameTimer:
    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.start_time = 0 
        # flags
        self.active = False
        self.function = func
        if autostart:
            self.activate()
        self.repeat = repeat

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def __bool__(self):
        return self.active
    
    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.function and self.start_time != 0:
                self.function()
            self.deactivate()