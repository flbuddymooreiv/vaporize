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

orgreds = []
allreds = []
sizes = []
while size > 1: #1 because dividing by 2 will never get us to 0
    size /= 2
    corners, ss = findnxns(ss,math.ceil(size))
    sizes += [[size,len(corners)]]
    targets = [(x+size/2, y+size/2) for (x,y) in corners]
    orgreds += [(size,targets)]
    allreds += targets

avgsize = sum([x[0] * x[1] for x in sizes])/len(allreds)

def dist(p1, p2): return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
def distpos(p): return dist(p, pos)

reds = allreds
reds = sorted(reds, key=distpos)
targets = [[False, x] for x in reds]
for t in targets:
    if not t[0]:
        pyautogui.click(x = t[1][0], y= t[1][1])
        for x in targets:
            if dist(t[1], x[1]) < avgsize*4:
                x[0] = True

# for orgred in orgreds:
#     reds = orgred[1]
#     reds = sorted(reds, key=distpos)
#     targets = [[False, x] for x in reds]
#     for t in targets:
#         if not t[0]:
#             pyautogui.click(x = t[1][0], y= t[1][1])
#             for x in targets:
#                 if dist(t[1], x[1]) < avgsize*8:
#                     x[0] = True
