from numpy import true_divide
import pygame as pg
import time

class displayMeasure():
    def __init__(self, displayObj, size, text): # current display, size as a ratio of minSize
        self.font = pg.freetype.SysFont("Courier New", 100, bold=True)
        self.screen = displayObj.screen
        self.text = text
        self.size = displayObj.minSize * size
        self.rect = self.font.get_rect(self.text, size = self.size)
        self.metrics = self.font.get_metrics(self.text)
        self.rect.center = self.screen.get_rect().center

    def move(self, x, y):
        self.rect.move(x, y)

    def updateSize(self, size):
        size = self.screen * size
        self.rect = self.font.get_rect(self.text, size = self.size)

    def updateText(self, measure): # measure of type list
        self.text = ""
        for textIdx in range(len(measure)):
            if textIdx != 0:
                self.text += " "
            self.text += str(measure[textIdx])

        self.rect = self.font.get_rect(self.text, size = self.size)
        self.metrics = self.font.get_metrics(self.text)

    def display(self, colors):
        if len(colors) != len(self.text):
            print("not enough colors")
            return
        x = self.rect.x
        for characterIdx in range(len(self.text)):
            self.font.render_to(self.screen, (x, self.rect.y), self.text[characterIdx], colors[characterIdx], size = self.size)
            x += self.metrics[characterIdx][4]
        
    

class display():
    def __init__(self):
        self.width = pg.display.Info().current_w
        self.height = pg.display.Info().current_h
        self.minSize = min(self.width, self.height)
        self.screen = pg.display.set_mode((self.width, self.height))

class Colors():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)



class Game():
    def __init__(self):
        pg.init()
        self.display = display()
        self.cl = Colors()
    def gameLoop(self):
        running = True

        measureTxt = "0 1 1 0 1 1"
        measure = displayMeasure(self.display, .1, measureTxt)

        while running:
            measureTxt = "0 1 1 0 1 1"
            colors = []
            for character in measureTxt:
                if character == "0":
                    colors.append(self.cl.red)
                elif character == "1":
                    colors.append(self.cl.green)
                else:
                    colors.append(self.cl.white)
            
            measure.display(colors)

            pg.display.flip()
            time.sleep(100)

game = Game()
game.gameLoop()

