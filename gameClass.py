import numpy as np
import pygame as pg
import time
from displayMeasure import displayMeasure
from display import display
from musicPlayer import MusicPlayer



class Colors():
    def __init__(self):
        self.emptyColor = (22, 22, 22) # empty beat
        self.currentColor = (100, 100, 100) # current beat
        self.backgroundColor = (255, 255, 255)
        self.decayColor = (200, 200, 200)
        self.beatHighLight = (177, 177, 177)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (200, 200, 200)

        self.red = (255, 0, 0)
        self.green = (92, 181, 92)
        self.blue = (2, 117, 221)
        self.yellow = (255, 200, 79)

        self.dred = tuple(i // 3 for i in self.red)
        self.dgreen = tuple(i // 3 for i in self.green)
        self.dblue = tuple(i // 3 for i in self.blue)
        self.dyellow = tuple(i // 3 for i in self.yellow)
        


class Key():
    def __init__(self, displayObj, color, colorPressed, key, id, cords, size):
        self.displayObj = displayObj
        self.color = color
        self.colorPressed = colorPressed
        self.key = key
        self.id = id
        self.x = cords[0]
        self.y = cords[1]
        self.rect = pg.Rect(self.x, self.y, size[0], size[1])
        self.state = 0
        

    def display(self):
        color = self.color
        if self.state == 1:
            color = self.colorPressed
        screen = self.displayObj.screen
        pg.draw.rect(screen, color, self.rect)
        



class Game():
    def __init__(self):
        pg.init()
        pg.display.set_caption("Rythm Game") # header
        self.display = display()
        self.screen = self.display.screen
        self.cl = Colors()

        self.bpm = 170
        self.beatsPerMeasure = 8 # beats per measure
        # self.minbeatDivision = 0.125 # shortest beat subdivision
        self.minbeatDivision = .5 # shortest beat subdivision

        # UI CONSTS
        self.measureWidth = 2
        self.decayScaling = .8
        self.decayColor = 1.5

        
        self.ticksPerBar = int(self.beatsPerMeasure/self.minbeatDivision) # ticks per bar
        self.tickLen = 60 / (self.bpm / self.minbeatDivision) # bpm / minbeatDivision = ticksPerMinute, ticksPerMinute/60 = ticsPerSecond, 1/ticsPerSecond = tickLen in seconds
        self.instrumentLen = 4 # keys used
        self.history = []
        self.running = True

        self.loseCondition = False

        self.keyMaker()

    def keyStep(self, idx, keySize, keysLen):
        width = self.display.width
        xCord = (1/(keysLen+1) * idx)*width - keySize
        return xCord
    def keyMaker(self):
        keySize = self.display.minSize // 20
        keyShape = (keySize * 2, keySize)
        keyHeight = ( self.display.height * (19/20) ) - keySize
        keysLen = 4
        # (1/(keyLen+1) * i) - keySize
        self.keys = { # key ids are 1 indexed
            pg.K_d: Key(self.display, self.cl.red, self.cl.dred, pg.K_d, 1, (self.keyStep(1, keySize, keysLen),keyHeight), keyShape),
            pg.K_f: Key(self.display, self.cl.green, self.cl.dgreen, pg.K_f, 2, (self.keyStep(2, keySize, keysLen),keyHeight), keyShape),
            pg.K_j: Key(self.display, self.cl.blue, self.cl.dblue, pg.K_j, 3, (self.keyStep(3, keySize, keysLen) - keySize,keyHeight), keyShape),
            pg.K_k: Key(self.display, self.cl.yellow, self.cl.dyellow, pg.K_k, 4, (self.keyStep(4, keySize, keysLen) - keySize,keyHeight), keyShape)
        }

    def refresh(self, elems):
        self.screen.fill(self.cl.backgroundColor)
        for elem in elems:
            elem.display()
        pg.display.flip()

    def moveHist(self):
        newHist = []
        for measure in self.history:
            measure.move(0, (-2 * measure.rect.h))
            if measure.rect.y > 0:
                newHist.append(measure)
        self.history = newHist
                
    def quantizer(self, measure, beatStart):
        for beatIdx in range(self.ticksPerBar): # for beat i in measure
                timeEnd = beatStart + self.tickLen # calc tick step
                oldColor = measure.colors[beatIdx]
                if measure.text[beatIdx] == "0":
                    measure.updateChar(beatIdx, "0", self.cl.currentColor)
                measure.center()
                measure.move(0, (self.display.height * 7/20) - measure.rect.h) # move 2/5 the screen height down from the center (add back hight of rect to move the bottom instead of top)
                self.refresh([measure] + list(self.keys.values()) + self.history)

                while time.time() < timeEnd: # while not tick
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            self.running = False
                            pg.quit()
                        if event.type == pg.KEYDOWN:
                            keyName = event.key
                            if keyName in self.keys.keys():
                                key = self.keys[keyName]
                                key.state = 1

                        if event.type == pg.KEYUP: # if key pressed
                            keyName = event.key

                            if keyName in self.keys.keys(): # Log Key
                                curTime = time.time()
                                key = self.keys[keyName]
                                key.state = 0

                                times = np.array([beatStart, timeEnd])
                                idx = (np.abs(times - curTime)).argmin() # if idx is 0, the beatIdx = beatIdx else beatIdx = beatIdx + 1
                                measure.updateChar( int((beatIdx + idx) % self.ticksPerBar), str(key.id), key.color)
                            elif keyName == pg.K_SPACE:
                                self.measureStart = time.time()
                                return measure
                if measure.text[beatIdx] == "0":
                    measure.updateChar(beatIdx, "0", oldColor)
                beatStart += self.tickLen
        return measure
    def printText(self, text, color):
        colors = []
        for elem in text:
            colors.append(color)
        measure = displayMeasure(self.display, .5, text, colors)
        measure.center()
        self.refresh([measure])
    def tempoInit(self):
        self.ticksPerBar = int(self.beatsPerMeasure/self.minbeatDivision) # ticks per bar
        self.tickLen = 60 / (self.bpm / self.minbeatDivision) # bpm / minbeatDivision = ticksPerMinute, ticksPerMinute/60 = ticsPerSecond, 1/ticsPerSecond = tickLen in seconds
    def gameLoop(self):
        self.chooseSong = True
        self.musicPlayer = MusicPlayer()
        curSongIdx = 0
        self.printText(self.musicPlayer.songs[curSongIdx], self.cl.black)
        while self.chooseSong:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP: # if key pressed
                    if event.key == pg.K_UP:
                        songName = self.musicPlayer.up()
                        self.printText(songName, self.cl.black)
                    elif event.key == pg.K_DOWN:
                        songName = self.musicPlayer.down()
                        self.printText(songName, self.cl.black)
                    elif event.key == pg.K_SPACE:
                        self.chooseSong = False

        if self.musicPlayer.getBpm() != 0:
            self.bpm = self.musicPlayer.getBpm()
            self.tempoInit()

        print(self.bpm)
        self.musicPlayer.reload()
        self.measureStart = time.time()
        while self.running:
            beatStart = self.measureStart
            self.measureStart += self.tickLen * self.ticksPerBar
            curMeasure = np.zeros(self.ticksPerBar, dtype = np.uint8)
            colors = []
            for i in range(len(curMeasure)):
                if i % self.beatsPerMeasure == 0:
                    colors.append(self.cl.beatHighLight)
                else:
                    colors.append(self.cl.emptyColor)

            measure = displayMeasure(self.display, self.measureWidth/len(curMeasure))
            measure.updateText(curMeasure, colors)

            '''
            for beatIdx in range(self.ticksPerBar): # for beat i in measure
                timeEnd = beatStart + self.tickLen # calc tick step
                
                measure.updateChar(beatIdx, "0", self.cl.currentColor)
                measure.center()
                measure.move(0, (self.display.height * 7/20) - measure.rect.h) # move 2/5 the screen height down from the center (add back hight of rect to move the bottom instead of top)
                self.refresh([measure] + list(self.keys.values()) + self.history)

                while time.time() < timeEnd: # while not tick
                    events = pg.event.get()
                    for event in events:
                        if event.type == pg.QUIT:
                            running = False
                            pg.quit()
                        if event.type == pg.KEYDOWN:
                            keyName = event.key
                            if keyName in self.keys.keys():
                                key = self.keys[keyName]
                                key.state = 1
                                print("pressed")

                        if event.type == pg.KEYUP: # if key pressed
                            keyName = event.key

                            if keyName in self.keys.keys():
                                key = self.keys[keyName]
                                key.state = 0
                                measure.updateChar(beatIdx, str(key.id), key.color)
                            elif keyName == pg.K_SPACE:
                                # RESET
                                continue
                if measure.text[beatIdx] == "0":
                    measure.updateChar(beatIdx, "0", self.cl.emptyColor)
                beatStart = time.time()
                # measure.updateChar(beatIdx, key.id, key.color)
                # measure.display()
                # pg.display.update()
            '''
            measure = self.quantizer(measure, beatStart)
            if self.loseCondition:
                hist = []
                for elem in self.history:
                    hist.append(elem.text)
                allZeros = all(beat == "0" for beat in measure.text)
                if not allZeros and measure.text in hist:
                    self.running = False
            measure.updateSize(  (self.measureWidth/ (len(curMeasure))) * self.decayScaling )
            measure.setDecayColor(self.cl.decayColor)
            measure.center()
            measure.move(0, (self.display.height * 6/20) - measure.rect.h) # move 2/5 the screen height down from the center (add back hight of rect to move the bottom instead of top)
            self.history.append(measure)
            self.moveHist()

        self.running = True
        while self.running:
            self.printText("GAME OVER", self.cl.red)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                            


game = Game()
game.gameLoop()

