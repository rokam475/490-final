import pygame as pg

class displayMeasure():
    def __init__(self, displayObj, size, text="", colors=[]): # current display, size as a ratio of minSize
        self.font = pg.freetype.SysFont("Courier New", 1000, bold=True) # font, args: font, resolution, bold
        self.displayObj = displayObj
        self.screen = displayObj.screen # screen surface
        self.text = text    # measure text
        self.colors = colors
        self.size = displayObj.minSize * size # caculate size as ratio of screen
        self.rect = self.font.get_rect(self.text, size = self.size) # get rect surface from font/text
        if self.rect.h > displayObj.minSize / 6:
            self.updateSize(1/6)
        self.metrics = self.font.get_metrics(self.text) # get letter metrics for given text
        self.rect.center = self.screen.get_rect().center # start measure off in center
    
    def scaleColor(self, factor):
        for idx in range(len(self.colors)):
            self.colors[idx] = tuple( min(i * factor, 255) for i in self.colors[idx])
    
    def setDecayColor(self, newColor):
        for idx in range(len(self.text)):
            if self.text[idx] == "0":
                self.colors[idx] = newColor


    def move(self, x, y):
        self.rect.move_ip(x, y) # move measure rect


    def updateSize(self, size):
        size = self.displayObj.minSize * size # caculate new size of rect
        size = int(size)
        self.size = size
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect

    def updateText(self, measure, colors): # measure of type list
        self.text = "" # clear text
        for textIdx in range(len(measure)): # loop through measure (list)
            self.text += str(measure[textIdx]) # append new character as string
        self.colors = colors # update
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect and metrics
        self.metrics = self.font.get_metrics(self.text)
        
    def updateChar(self, idx, character, color):
        charList = list(self.text)
        charList[idx] = character
        self.text = "".join(charList) # update char
        self.colors[idx] = color # update color
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect and metrics
        self.metrics = self.font.get_metrics(self.text)
    
    def center(self):
        self.rect.center = self.screen.get_rect().center # start measure off in center
    
    def highlight(self, idx, color):
        x = self.rect.x
        x += self.rect.w//len(self.text) * idx
        self.font.render_to(self.screen, (x, self.rect.y), self.text[idx], color, size=self.size)

    def display(self):
        x = self.rect.x # start x = x cord of rect
        for characterIdx in range(len(self.text)): # loop though text
            # render to: screen, at cords (x, rect y), indexed character, indexed color, size
            self.font.render_to(self.screen, (x, self.rect.y), self.text[characterIdx], self.colors[characterIdx], size=self.size)
            x += self.rect.w//len(self.text)
            # x += self.metrics[characterIdx][4] # increase x by character length (metric at character idx), 4 gets the width