import pygame as pg

class display():
    def __init__(self):
        self.width = pg.display.Info().current_w
        self.height = pg.display.Info().current_h
        self.minSize = min(self.width, self.height)
        self.screen = pg.display.set_mode((self.width, self.height))