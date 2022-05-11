import time
import pygame as pg
from pygame import mixer
import numpy as np
from random import randint
from utils import quantizer

class Key():
    def __init__(self,  color, colorPressed, key):
        self.color = color
        self.colorPressed = colorPressed
        self.key = key
        self.rect = pg.Rect(self.x, self.y, 50, 20)

class Colors():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

CL = Colors()

KEYS = [
    Key(CL.red, CL.white, pg.K_d),
    Key(CL.green, CL.white, pg.K_f),
    Key(CL.blue, CL.white, pg.K_j),
    Key(CL.yellow, CL.white, pg.K_k)
]

pg.init()
WIDTH, HEIGHT = pg.display.get_surface().get_size()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))


def gameLoop():
    running = True
    # init segment
    bpm = 200 # bpm
    measure = 4 # beats per measure
    minFreq = 0.125 # shortest beat subdivision

    ticksPerBar = int(measure/minFreq) # ticks per bar
    tps = (bpm / minFreq) /60 # ticks per minute
    beatLen = 1 / tps # length of a single beat in seconds

    history = []
    while running:
       
       pg.display.update()
