import pygame as pg

class display(): # houses display and screen surface info
    def __init__(self):
        self.width = pg.display.Info().current_w # get display width
        self.height = pg.display.Info().current_h # get display width
        self.minSize = min(self.width, self.height) # minimum of both dimensions (reference for bounds/sizing)
        self.screen = pg.display.set_mode((self.width, self.height)) # screen object that matches the current display