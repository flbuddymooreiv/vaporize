#!/usr/bin/env python3

import time
import math
import pyautogui

import random
from PIL import Image, ImageChops
from enum import Enum

import pytesseract
import numpy as np
import cv2

pyautogui.PAUSE = 0.05
UPS_THRESHOLD=25

origpos = pyautogui.mouseinfo.position()

ss = pyautogui.screenshot()
fifthwidth = ss.width/5
fifthheight = ss.height/5
def zoneviz():
    global fifthwidth, fifthheight
    pyautogui.moveTo(fifthwidth, fifthheight)
    time.sleep(.1)
    pyautogui.moveTo(fifthwidth * 4, fifthheight)
    time.sleep(.1)
    pyautogui.moveTo(fifthwidth * 4, fifthheight * 4)
    time.sleep(.1)
    pyautogui.moveTo(fifthwidth, fifthheight * 4)
    time.sleep(.1)

class Mode(Enum):
    ONE_THIRD_ARC_SWEEP = 1
    AFK_GRIND = 2
    TWO_THIRD_ARC_SWEEP = 3
    ONE_HALF_ARC_SWEEP = 4
    NINETY_PCT_ARC_SWEEP = 5

#mode = Mode.NINETY_PCT_ARC_SWEEP
#mode = Mode.TWO_THIRD_ARC_SWEEP
mode = Mode.ONE_THIRD_ARC_SWEEP
#mode = Mode.ONE_HALF_ARC_SWEEP
#mode = Mode.AFK_GRIND

def dist(p1, p2): return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
def arcdist(p1, p2): return math.atan2(p1[0] - p2[0], p1[1] - p2[1])
def distpos(p): return dist(p, origpos)
def arcdistpos(p): return arcdist(p, origpos)
def extentsize(p): return math.sqrt((p[2] ** 2) + (p[3] ** 2))
def extentsizethenarcdistpos(p): return (extentsize(p) * 10000) + arcdistpos(p)

def sleep():
    #time.sleep(0.2/float(fps))
    #time.sleep(0.05)
    time.sleep(0.01)
    
def get_ups():
    return 60
    data = None
    with open('/home/buddy/vaporize/ups.txt', 'r') as f:
        data = f.read()
    return data

def parse_ups(data):
    try:
        nums = data.split(' ')[2]
        fps = float(nums.split('/')[0])
        ups = float(nums.split('/')[1])
        return (fps,ups)
    except Exception as e:
        print(e)
        pass
    return (-1,-1)
        

def ok_to_shoot():
    # uncomment to override
    return True

    data = get_ups()
    if data:
        (fps,ups) = parse_ups(data)
        return ups > UPS_THRESHOLD and fps > .33 * ups
    return False

currss = None 
prevss = None

def loop():
    global currss, prevss
    data = get_ups()
    #(fps,ups) = parse_ups(data)

    #if fps<0: return

    pos = pyautogui.mouseinfo.position()
    pyautogui.moveTo(fifthwidth * 4, fifthheight * 4)
    sleep()

    prevss = currss
    currss = pyautogui.screenshot()

    if prevss and currss:
        # black out the differences so we only see stationary targets
        ss = ImageChops.subtract(currss, prevss)
        ss = ImageChops.subtract(currss, ss)
        pyautogui.moveTo(pos)
        ss = ss.crop((fifthwidth,fifthheight,fifthwidth * 4,fifthheight * 4))
        #ss.save('ss.png')

        def enoughredpixel(p):
            return p[0] >= 96 and p[1] < 32 and p[2] < 32
        def enoughred(region,x,y):
            try:
                return enoughredpixel(region.getpixel((x,y)))
            except Exception as e:
                print(e)
                return False

        pixels = []
        bigpixels = []
        biggerpixels = []
        region = ss
        extents = {}

        def putp(r, x, y, c=(0,255,0,0)):
            try:
                r.putpixel(x,y,c)
            except Exception as e:
                print(e)
                pass

        for i in range(0,math.floor(region.width)-1):
            for j in range(0,math.floor(region.height)-1):
                extent = 0
                extentx = 0
                extenty = 0
                fits = True

                while fits:
                    if enoughred(region, i + extentx, j):
                        extentx += 1
                    if enoughred(region, i, j + extenty):
                        extenty += 1
                    else:
                        fits = False
                        if extentx > 0 or extenty > 0:
                            region.paste((0,255,0,0), [i,j,i+extentx,j+extenty])

                            extent = math.sqrt(extentx * extentx + extenty * extenty)

                            if extent not in extents: extents[extent] = []
                            extents[extent] += [[i,j,extentx,extenty]]

        #region.save('parsed.jpg')

        clicks = [c for l in list(extents.values()) for c in l ]
        if mode == Mode.AFK_GRIND:
            n = len(clicks)
            #clicks = sorted(clicks, key=distpos)
            #clicks = clicks[:int(len(clicks)/3)]
            clicks = list(reversed(sorted(clicks, key=extentsize)))
            #clicks = clicks[:int(len(clicks)/8)]
            #random.shuffle(clicks)
            clicks = clicks[:int(math.sqrt(n))]
            clicks = sorted(clicks, key=arcdistpos)
        else:
            portion = 1
            if mode == Mode.NINETY_PCT_ARC_SWEEP:
                portion = 0.90
            elif mode == Mode.TWO_THIRD_ARC_SWEEP:
                portion = 0.66
            elif mode == Mode.ONE_HALF_ARC_SWEEP:
                portion = 0.5
            elif mode == Mode.ONE_THIRD_ARC_SWEEP:
                portion = 0.33

            clicks = sorted(clicks, key=extentsize)
            clicks = list(reversed(clicks))[:math.floor(len(clicks) * portion)]
            clicks = sorted(clicks, key=arcdistpos)
            #clicks = sorted(clicks, key=arcdistpos)
            #clicks = reversed(sorted(clicks, key=axtentsize))
        extentmap = {}
        for k in extents:
            for p in extents[k]:
                extentmap[str(p)] = k

        weightedextents = sum([k * len(extents[k][0]) for k in extents.keys()])
        totalpoints = sum([len(extents[k][0]) for k in extents.keys()])

        threshextent = (weightedextents / totalpoints * 0.33) if totalpoints else 0

        for c in clicks:
            extent = extentmap[str(c)]
            #print(c)
            #if extent > threshextent:
            pyautogui.click(
                x = fifthwidth + (c[0] + c[2]/2), 
                y = fifthheight + (c[1] + c[3]/2))
            # sleep()
            #extent = extentmap[str(c)]
            #if extent > threshextent:
            #    for i in range(0, int(extent/threshextent) + 1):
            #        for j in range(0, int(extent/threshextent) + 1):
            #            pyautogui.click(x = c[0] + i * threshextent, y= c[1] + j * threshextent)

        #pyautogui.moveTo(pos)

zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()
zoneviz()

if mode == Mode.AFK_GRIND:
    while True:
        if ok_to_shoot(): loop()
        time.sleep(.1)
else:
    #first loop primes first screenshot for comparison
    loop()
    loop()
