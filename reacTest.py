import time
import pygame as pg
from pygame import mixer
import numpy as np
from pythonosc import udp_client
from random import randint
screen = pg.display.set_mode((800, 600))
times = []
lastHit = time.time()
running = True
while running:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                print(times)
                print(min(times))
                pg.quit()

            if event.type == pg.KEYUP:
                curTime = time.time()
                print("hit")
                times.append(curTime - lastHit)
                lastHit = curTime
                
