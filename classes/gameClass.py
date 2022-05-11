import numpy as np
import pygame as pg
import time
from displayMeasure import displayMeasure
from display import display

class Colors():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

class Key():
    def __init__(self, color, colorPressed, key, id, cords):
        self.color = color
        self.colorPressed = colorPressed
        self.key = key
        self.id = id
        self.x = cords[0]
        self.y = cords[1]
        self.rect = pg.Rect(self.x, self.y, 50, 20)



class Game():
    def __init__(self):
        pg.init()
        self.display = display()
        self.cl = Colors()

        self.bpm = 200
        self.beatsPerMeasure = 4 # beats per measure
        self.minbeatDivision = 0.125 # shortest beat subdivision

        self.ticksPerBar = int(self.beatsPerMeasure/self.minbeatDivision) # ticks per bar
        self.tickLen = 60 / (self.bpm / self.minbeatDivision) # bpm / minbeatDivision = ticksPerMinute, ticksPerMinute/60 = ticsPerSecond, 1/ticsPerSecond = tickLen in seconds
        self.instrumentLen = 4 # keys used
        self.history = []

        self.keys = {
            pg.K_d: Key(self.cl.red, self.cl.white, pg.K_d, 0, (0,0)),
            pg.K_f: Key(self.cl.green, self.cl.white, pg.K_f, 1, (0,0)),
            pg.K_j: Key(self.cl.blue, self.cl.white, pg.K_j, 2, (0,0)),
            pg.K_k: Key(self.cl.yellow, self.cl.white, pg.K_k, 3, (0,0))
        }


    def gameLoop(self):
        running = True

        while running:
            measureStart = time.time()
            beatStart = measureStart
            curMeasure = np.zeros(self.ticksPerBar, dtype = np.uint8)
            curMeasure = np.zeros(8, dtype = np.uint8)

            curMeasure[0] = 1
            curMeasure[-1] = 1


            colors = []
            for idx in range(len(curMeasure)):
                if curMeasure[idx] == "0":
                    colors.append(self.cl.red)
                elif curMeasure[idx] == "1":
                    colors.append(self.cl.green)
                else:
                    colors.append(self.cl.white)

            measure = displayMeasure(self.display, 2/len(curMeasure))
            measure.updateText(curMeasure, colors)
            measure.center()
            measure.display()

            pg.display.flip()
            time.sleep(100)

game = Game()
game.gameLoop()

