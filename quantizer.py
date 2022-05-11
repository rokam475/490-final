import time
import pygame
from pygame import mixer
import numpy as np
from pythonosc import udp_client
from random import randint
client = udp_client.SimpleUDPClient("127.0.0.1", 57120) #default ip and port for SC

#mixer.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

hihat = mixer.Sound('mp3\hihat.mp3')
drum = mixer.Sound('mp3\drum.mp3')

print(hihat)


screen = pygame.display.set_mode((800, 600))

class bar():
    def __init__(self, size, length):
        self.size = size
        self.length = length
        self.elems = []

        

class Key():
    def __init__(self, x, y, color, colorPressed, key, sound):
        self.x = x
        self.y = y
        self.color = color
        self.colorPressed = colorPressed
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 50, 20)
        self.sound = sound
        

keys = [
    Key(100, 500, (0,255,0),(255,255,255),pygame.K_f, drum),
    Key(650, 500, (0,255,0),(255,255,255),pygame.K_j, hihat)
]

bpm = 200 # bpm
measure = 4 # beats per measure
minFreq = 0.125 # shortest beat subdivision
ticksPerBar = int(measure/minFreq) # ticks per bar

tps = (bpm / minFreq) /60 # ticks per minute
beatLen = 1 / tps # length of a single beat in seconds

print("BEAT LEN IS:")
print(beatLen)

oldCalibeat = 0 # old start beat
caliBeat = 0 # start beat
caliCount = 0 # current number of correct beats
caliReq = 3 # required number of correct beats in a row

print("CALIBRATING")

while caliCount < caliReq: # while current number of currect beats is less than the required
    print(caliBeat)
    if caliBeat == oldCalibeat: # if the old calibeat matches new, inc count 
        caliCount += 1
    else:                   # else reset count
        caliCount = 0

    drum.play()     # play measure start beat
    for i in range(ticksPerBar): # for beat i in the measure

        tend = time.time() + beatLen # calc next tick
        while time.time() < tend: # while not next tick
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYUP: # if key pressed
                    if i == 1:
                        caliBeat = 1    # i is the start beat

print("FINISHED CALIBRATING")
print(caliBeat)


# print("CALIBRATING")
# targetLatency = .1
# measureLength = beatLen*ticksPerBar
# while True:

# print("FINISHED CALIBRTING")


# beat game
oldMeasure = np.zeros(ticksPerBar) # past measure
curMeasure = np.zeros(ticksPerBar) # current measure (to log current beats)

measureStart = 0

while True:
    '''
    
    print(time.time() - measureStart)
    measureStart = time.time()
    oldMeasure = curMeasure # set old measure to the current measure
    curMeasure = np.zeros(ticksPerBar) # clear current measure
    
    print(oldMeasure) # print measure to be played
    '''
    measureStart = time.time()
    print(curMeasure)
    curMeasure = np.zeros(ticksPerBar)

    # track measure timing
    
    


    for i in range(ticksPerBar): # for beat i in measure
        if i == caliBeat: # if i == the calibreated beat
            
            # drum.play()     # play measure start beat
            continue

        if oldMeasure[i] != 0: # if old measure is 1 on the current beat
            continue
            #hihat.play() # play hi hat

        tend = time.time() + beatLen # calc tick step
        while time.time() < measureStart + ((i+1) * beatLen): # while not tick
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP: # if key pressed
                    curMeasure[i] = 1   # log key
                    print("PRESSED")
                    # hihat.play()
                    client.send_message("/send", randint(300, 700)) # set the frequency at 440




        



# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
    
#     pressedKeys = pygame.key.get_pressed()
#     # for event in pygame.event.get():
#     #     if event.type == pygame.KEYUP:
#     #         print("pressed")
#     #         hihat.play()

#     for key in keys:    
#         if pressedKeys[key.key]:
#             print(pressedKeys)
#             pygame.draw.rect(screen, key.colorPressed, key.rect)
#             print(key.key)
#             key.sound.play()
#         elif not pressedKeys[key.key]:
#             pygame.draw.rect(screen, key.color, key.rect)

    pygame.display.update()