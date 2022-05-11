import pygame as pg
import numpy as np

pg.init()
WIDTH = pg.display.Info().current_w
HEIGHT = pg.display.Info().current_h
MINSIZE = min(WIDTH, HEIGHT)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
def sizer(size):
    return MINSIZE * size

def displayList(orgList, size):
    returnText = ""
    for textIdx in range(len(orgList)):
        if textIdx != 0:
            returnText += " "
        returnText += str(orgList[textIdx])
    
    returnText = myFont.render_to(returnText, True, black)
    return scaler(returnText, size)
        
    
def scaler(surface, size):
    w, h = surface.get_size()
    ratio = h/w
    newWidth = MINSIZE * size
    newImg = pg.transform.smoothscale(surface, (newWidth, newWidth * ratio))
    return newImg


count = 0
white = (255, 255, 255)
black = (0, 0, 0)
myFont = pg.font.SysFont("Courier New", 100, bold=True)
myFont = pg.freetype.SysFont("Courier New", 100, bold=True)

while True:
    count += 1
    measure = [count, 0, 0, 0, 0]

    SCREEN.fill(white)
    tempMes = displayList(measure, .3)
    SCREEN.blit(tempMes, (0, 0))

    pg.display.update()


