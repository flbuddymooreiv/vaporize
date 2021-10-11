#!/usr/bin/env python3

import time
import math
import pyautogui

import random
from PIL import Image

import pytesseract
import numpy as np
import cv2

pyautogui.PAUSE = 0.5
UPS_THRESHOLD=30

pos = pyautogui.mouseinfo.position()

def dist(p1, p2): return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
def arcdist(p1, p2): return math.atan2(p1[0] - p2[0], p1[1] - p2[1])
def distpos(p): return dist(p, pos)
def arcdistpos(p): return arcdist(p, pos)


def ok_to_shoot():
    with open('/home/buddy/vaporize/ups.txt', 'r') as f:
        data = f.read()
    if data:
        try:
            nums = data.split(' ')[2]
            fps = float(nums.split('/')[0])
            ups = float(nums.split('/')[1])
            print(fps, ups)
            return ups > UPS_THRESHOLD and fps > .33 * ups
        except Exception as e:
            print(e)
            pass
    return False

def loop():
    ss = pyautogui.screenshot()
    ss = ss.crop((0,0,1665,919))
    #ss.save('ss.png')

    def enoughredpixel(p):
        return p[0] >= 96 and p[1] < 32 and p[2] < 32
    def enoughred(region,x,y):
        try:
            return enoughredpixel(region.getpixel((x,y)))
        except:
            return False

    pixels = []
    bigpixels = []
    biggerpixels = []
    region = ss
    extents = {}

    def putp(r, x, y, c=(0,255,0,0)):
        try:
            r.putpixel(x,y,c)
        except:
            pass

    for i in range(0,math.floor(region.width)-1):
        for j in range(0,math.floor(region.height)-1):
            extent = 0
            fits = True

            while fits:
                if \
                   enoughred(region, i + extent, j) or \
                   enoughred(region, i - extent, j) or \
                   enoughred(region, i, j + extent) or \
                   enoughred(region, i, j - extent): 

                    extent += 1
                else:
                    fits = False
                    if extent > 0:
                        region.paste((0,255,0,0), [i-extent,j-extent,i+extent,j+extent])

                        if extent not in extents: extents[extent] = []
                        extents[extent] += [[i,j]]

    #region.save('parsed.jpg')

    clicks = [c for l in list(extents.values()) for c in l ]
    #clicks = sorted(clicks, key=arcdistpos)
    clicks = sorted(clicks, key=distpos)
    extentmap = {}
    for k in extents:
        for p in extents[k]:
            extentmap[str(p)] = k

    weightedextents = sum([k * len(extents[k][0]) for k in extents.keys()])
    totalpoints = sum([len(extents[k][0]) for k in extents.keys()])

    threshextent = weightedextents/totalpoints/2 if totalpoints else 0

    #random.shuffle(clicks)
    #clicks = clicks[:10]

    clicks = clicks[:100]
    random.shuffle(clicks)
    clicks = clicks[:10]

    print(clicks)

    for c in clicks:
        pyautogui.click(x = c[0], y= c[1])
        extent = extentmap[str(c)]
        if extent > threshextent:
            for i in range(0, int(extent/threshextent) + 1):
                for j in range(0, int(extent/threshextent) + 1):
                    pyautogui.click(x = c[0] + i * threshextent, y= c[1] + j * threshextent)
    pyautogui.moveTo(pos)


while True:
    if ok_to_shoot(): loop()
    time.sleep(1)
