import pygame as pg
import numpy as np

pg.init()
WIDTH = pg.display.Info().current_w
HEIGHT = pg.display.Info().current_h
MINSIZE = min(WIDTH, HEIGHT)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
myFont = pg.freetype.SysFont("Courier New", 100, bold=True)

def drawTextCentered(surface, text, text_size, color):
    text_rect = myFont.get_rect(text, size = 50)
    metrics = myFont.get_metrics(text)
    text_rect.center = surface.get_rect().center
    x = 0
    for characterIdx in range(len(text)):
        color = (255, 255, 255)
        if text[characterIdx] == "0":
            color = (255, 0, 0)
        elif text[characterIdx] == "1":
            color = (0, 255, 0)
        myFont.render_to(surface, (x, text_rect.y), text[characterIdx], color, size = 50)
        x += metrics[characterIdx][4]

while True:

    drawTextCentered(SCREEN, "0 0 1 1 0 1 0", 50, (255, 0, 0))  

    pg.display.update()



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
    testText = "0 1 0 0 1 1 0"
    text_surf = pg.Surface(myFont.get_rect(testText).size)
    for character in testText:
        color = (255, 255, 255)
        if character == "0":
            color = (255, 0, 0)
        elif character == "1":
            color = (0, 255, 0)
        myFont.render_to(text_surf, myFont.get_rect(testText), character, color)


    text = "Hello World"
    text_size = 50
    text_rect = myFont.get_rect(text, size = text_size)

    myFont.render_to(surface, text_rect, text, color, size = text_size)
    SCREEN.fill(white)
    tempMes = displayList(measure, .3)
    SCREEN.blit(text_surf, (0, 0))


    pg.display.update()


