import time
import numpy as np
import pygame as pg

def displayMeasure(keys, measure):
    displayMeasure = []
    for beatIdx in range(measure.shape[1]):
        color = np.asarray((0, 0, 0))
        for keyIdx in range(measure.shape[0]):
            color += keys[keyIdx]





def buildKeyMap(keys):
    keyMap = {}
    keyIdx = 0
    for key in keys:
        keyMap[key] = keyIdx
        keyIdx += 1
    return keyMap


def quantizer(ticks, beatLen, instrumentLen, keys):
    measureStart = time.time()
    # print(curMeasure)
    beatStart = measureStart
    measureLen = np.zeros(ticks)
    curMeasure = np.zeros([instrumentLen, measureLen])

    keyMap = {}
    keyIdx = 0
    for key in keys:
        keyMap[key] = keyIdx
        keyIdx += 1
    # track measure timing


    for beatIdx in range(measureLen): # for beat i in measure
        timeEnd = beatStart + beatLen # calc tick step
        while time.time() < timeEnd: # while not tick
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP: # if key pressed
                    keyName = event.key
                    keyIdx = -1
                    if keyName in keyMap.keys():
                        keyIdx = keyMap[keyName]
                    if keyIdx != -1:
                        curMeasure[keyIdx, beatIdx] = 1
                    print("PRESSED")
    return curMeasure
