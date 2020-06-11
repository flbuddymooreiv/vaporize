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

def is_the_square_red(region, i, j, n): 
    #as soon as we find a non red pixel we immediately exit the loop
    try:
        for x in range(1,n):
            for y in range(1,n):
                if not enoughred(region.getpixel((i+x,j+y))):
                    return False				
    except IndexError as e:
        return False
    return True
           
i = 0
j = 0
first_square_found = dict()
def findnxn_new(region, n):
    #we remember the coordinates of the previously found square and continue searching for these coordinates
    global i, j, first_square_found
    while i < math.floor(region.width)-1:
        while j < math.floor(region.height)-1:
            p = region.getpixel((i,j))
            if enoughred(p):
                if is_the_square_red(region, i, j, n):
                    first_square_found[n] = [ i,j ]
                    return True
            j += 1
        i += 1
        j = 0
    return False

def findnxns(region, n):
    corners = []
    region = region.copy()
    #we continue the search with the coordinates that we have memorized in findnxn_new(region, n)
    i = first_square_found[n][0] 
    j = first_square_found[n][1]
    while i < math.floor(region.width)-1:
        while j < math.floor(region.height)-1:
            p = region.getpixel((i,j))
            if enoughred(p):
                try:
                    if is_the_square_red(region, i, j, n): 
                        #fill in the rectangle
                        corners += [[int(i+n*7/5/2),int(j+n/2)]]
                        for x in range(0, int(n*7/5) ):
                            for y in range(0,n):
                                region.putpixel((i+x,j+y), (0,0,0))
                except IndexError as e:
                    pass
            j += 1
        i += 1
        j = 0
    return corners, region


size = 1

while findnxn_new(ss,size): 
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
def arcdist(p1, p2): return math.atan2(p1[0] - p2[0], p1[1] - p2[1])
def distpos(p): return dist(p, pos)
def arcdistpos(p): return arcdist(p, pos)

reds = allreds
reds = sorted(reds, key=arcdistpos)
targets = [[False, x] for x in reds]

pyautogui.PAUSE = .2

for t in targets:
    if not t[0]:
        pyautogui.click(x = t[1][0], y= t[1][1])
        for x in targets:
            if dist(t[1], x[1]) < avgsize*2:
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
