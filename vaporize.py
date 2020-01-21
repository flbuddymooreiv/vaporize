#!/usr/bin/env python3

import os
import sys
import math
import pyautogui
from PIL import Image
import random

targets = int(sys.argv[1])
ss = pyautogui.screenshot()
ss = ss.crop((0,0,1672,919))
ss.save('ss.png')
pos = pyautogui.mouseinfo.position()

def enoughred(p):
    return p[0] >= 96 and p[1] < 32 and p[2] < 32

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
    

size = 1
reds = []

while findnxn(ss,size): 
    size *= 2
    os.system('notify-send -t 1000 "Finding targets: ' + str(size) + '"')

reds = []
while len(reds) < targets and size > 0:
    size /= 2
    corners, ss = findnxns(ss,math.ceil(size))
    reds += [(x+size/2, y+size/2) for (x,y) in corners]

os.system('notify-send "Randomizing targets"')
#random.shuffle(reds)
#for r in reds[0:targets]: pyautogui.click (x = r [0], y = r [1])
def dist(p): return math.sqrt(math.pow(p[0] - pos[0], 2) + math.pow(p[1] - pos[1], 2))
reds = sorted(reds, key=dist)
#print(reds)
for r in reds: pyautogui.click (x = r [0], y = r [1])
