#!/usr/bin/env python3

import os
import math
import pyautogui
from PIL import Image
import random

ss = pyautogui.screenshot()
ss = ss.crop((0,0,1672,919))
#ss = Image.open('ss.png')
ss.save('ss.png')

#### superfine
#xchunks = 400; ychunks = 300; thresh=.01
#### superfine
#xchunks = 200; ychunks = 150; thresh=.05
#### fine
#xchunks = 160; ychunks = 120; thresh=.03
#### medium
#xchunks = 80; ychunks = 60; thresh=.02
#### coarse
#xchunks = 60; ychunks = 30; thresh=.01
#### ultracoarse
xchunks = 10; ychunks = 20; thresh=.005

def enoughred(p):
    return p[0] >= 96 and p[1] < 32 and p[2] < 32

def findred(region):
    redpixels = []
    for i in range(0,math.floor(region.width)-1):
        for j in range(0,math.floor(region.height)-1):
            p = region.getpixel((i,j))
            if enoughred(p):
                redpixels += [(i,j)]

    if len(redpixels):
        random.shuffle(redpixels)
        return redpixels[0]
    return None
            
def findnxn(region, n):
    for i in range(0,math.floor(region.width)-1):
        for j in range(0,math.floor(region.height)-1):
            p = region.getpixel((i,j))
            if enoughred(p):
                search=[]
                try:
                    for x in range(0,n):
                        for y in range(0,n):
                            p = region.getpixel((i+x,j+y))
                            search += [p]
                    if all([enoughred(p) for p in search]):
                        return True
                except IndexError as e:
                    pass
    return False

def findnxns(region, n):
    corners = []
    region = region.copy()
    for i in range(0,math.floor(region.width)-1):
        for j in range(0,math.floor(region.height)-1):
            p = region.getpixel((i,j))
            if enoughred(p):
                try:
                    search=[]
                    for x in range(0,n):
                        for y in range(0,n):
                            p = region.getpixel((i+x,j+y))
                            search += [p]
                    if all([enoughred(p) for p in search]):
                        corners += [[i,j]]
                        for x in range(0,n):
                            for y in range(0,n):
                                region.putpixel((i+x,j+y), (0,0,0))
                except IndexError as e:
                    pass
    return corners, region
    

#chunkx = ss.width/xchunks
#chunky = ss.height/ychunks
#reds = []
#for x in range(0,xchunks):
#    for y in range(0,ychunks):
#        posx = chunkx * x
#        posy = chunky * y
#        region = ss.copy().crop((posx, posy, posx+chunkx, posy+chunky))
#        target = findred(region)
#        if target:
#            reds += [(posx + target[0] + 1, posy + target[1] + 1)]

size = 1
reds = []

while findnxn(ss,size): 
    size *= 2
    os.system('notify-send -t 1000 "Finding targets: ' + str(size) + '"')

reds = []
while len(reds) < 100 and size > 0:
    size /= 2
    corners, ss = findnxns(ss,math.ceil(size))
    reds += [(x+size/2, y+size/2) for (x,y) in corners]

os.system('notify-send "Randomizing targets"')
random.shuffle(reds)
os.system('notify-send "Generating Commands"')
for r in reds[0:100]:
    print('xdotool mousemove ' + str(r[0]) + ' ' + str(r[1]) + ' mousedown 1')
    print('sleep .05')
    #print('sleep .1')
    print('xdotool mouseup 1')
    print('sleep .05')
    #print('sleep .1')

