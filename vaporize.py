#!/usr/bin/env python3

import math
import pyautogui
from PIL import Image

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

while findnxn(ss,size): 
    size *= 2

reds = []
while size > 1: #1 because dividing by 2 will never get us to 0
    size /= 2
    corners, ss = findnxns(ss,math.ceil(size))
    reds += [(x+size/2, y+size/2) for (x,y) in corners]

def dist(p1, p2): return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
def distpos(p): return dist(p, pos)
reds = sorted(reds, key=distpos)
for r in reds:
    pyautogui.click(x = r[0], y= r[1])
