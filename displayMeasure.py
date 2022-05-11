import pygame as pg

class displayMeasure(): # object for each measure
    def __init__(self, displayObj, size, text="", colors=[]): # current display, size as a ratio of minSize
        self.font = pg.freetype.SysFont("DejaVu Sans Mono", 1000, bold=True) # font, args: font, resolution, bold
        self.displayObj = displayObj # physical display object
        self.screen = displayObj.screen # screen surface
        self.text = text    # measure text
        self.colors = colors # corrisponding colors
        self.size = displayObj.minSize * size # caculate size as ratio of screen
        self.rect = self.font.get_rect(self.text, size = self.size) # get rect surface from font/text
        if self.rect.h > displayObj.minSize / 6: # if rect is > 1/6th the minsize
            self.updateSize(1/6)    # truncate to 1/6th
        self.metrics = self.font.get_metrics(self.text) # get letter metrics for given text
        self.rect.center = self.screen.get_rect().center # start measure off in center
    
    def scaleColor(self, factor): # scale color of scale
        for idx in range(len(self.colors)): # loop through colors
            self.colors[idx] = tuple( min(i * factor, 255) for i in self.colors[idx]) # multiply by some factor and truncate at 255
    
    def setDecayColor(self, newColor): # set collor for history measures
        for idx in range(len(self.text)):   # loop though text
            if self.text[idx] == "0": # if the beat is empty
                self.colors[idx] = newColor # set it to decay color


    def move(self, x, y): # move measure rect
        self.rect.move_ip(x, y)


    def updateSize(self, size): # scale measure size
        size = self.displayObj.minSize * size # caculate new size of rect
        size = int(size)    # cast to int
        self.size = size    # update size
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect

    def updateText(self, measure, colors): # measure of type list
        self.text = "" # clear text
        for textIdx in range(len(measure)): # loop through measure (list)
            self.text += str(measure[textIdx]) # append new character as string
        self.colors = colors # update
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect and metrics
        self.metrics = self.font.get_metrics(self.text) # update text metrics
        
    def updateChar(self, idx, character, color): # update single character
        charList = list(self.text)  # cast text to list to idx elem
        charList[idx] = character   # replace character
        self.text = "".join(charList) # update text from list
        self.colors[idx] = color # update color
        self.rect = self.font.get_rect(self.text, size = self.size) # update rect and metrics
        self.metrics = self.font.get_metrics(self.text) # update text metrics
    
    def center(self):
        self.rect.center = self.screen.get_rect().center # start measure off in center
    
    def highlight(self, idx, color):
        x = self.rect.x # get rect starting pos
        x += self.rect.w//len(self.text) * idx  # caculate letter offset
        self.font.render_to(self.screen, (x, self.rect.y), self.text[idx], color, size=self.size) # render specific letter a different color

    def display(self): # display measure
        x = self.rect.x # start x = x cord of rect
        for characterIdx in range(len(self.text)): # loop though text
            # render to: screen, at cords (x, rect y), indexed character, indexed color, size
            self.font.render_to(self.screen, (x, self.rect.y), self.text[characterIdx], self.colors[characterIdx], size=self.size)
            x += self.rect.w//len(self.text) # add portion of rec corresponding to 1 letter
            # x += self.metrics[characterIdx][4] # increase x by character length (metric at character idx), 4 gets the width