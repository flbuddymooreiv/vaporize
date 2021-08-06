#!/usr/bin/env python3

import math
import pyautogui
import random
from PIL import Image

import pytesseract
import numpy as np
import cv2

while True:

    # filename = 'image_01.png'
    # img1 = np.array(Image.open(filename))
    # text = pytesseract.image_to_string(img1)

    # filename = 'image_02.png'
    # img2 = np.array(Image.open(filename))
    # text = pytesseract.image_to_string(img2)
    # norm_img = np.zeros((img.shape[0], img.shape[1]))

    # img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    # img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    # img = cv2.GaussianBlur(img, (1, 1), 0)
    # text = pytesseract.image_to_string(img)

    ss = pyautogui.screenshot()
    upsx1 = 1328
    upsx2 = 1399
    upsy1 = 73
    upsy2 = 92
    ups = ss.crop((upsx1,upsy1,upsx2-upsx1,upsy2-upsy1))
#    text = pytesseract.image_to_string(ups)

#    break

    ss = ss.crop((0,0,1665,919))
    #ss.save('ss.png')
    pos = pyautogui.mouseinfo.position()

    def dist(p1, p2): return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
    def arcdist(p1, p2): return math.atan2(p1[0] - p2[0], p1[1] - p2[1])
    def distpos(p): return dist(p, pos)
    def arcdistpos(p): return arcdist(p, pos)

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
    clicks = sorted(clicks, key=arcdistpos)
    extentmap = {}
    for k in extents:
        for p in extents[k]:
            extentmap[str(p)] = k

    weightedextents = sum([k * len(extents[k][0]) for k in extents.keys()])
    totalpoints = sum([len(extents[k][0]) for k in extents.keys()])

    avgextent = weightedextents/totalpoints

    for c in clicks:
        pyautogui.click(x = c[0], y= c[1])
        extent = extentmap[str(c)]
        if extent > avgextent:
            for i in range(0, int(extent/avgextent)):
                for j in range(0, int(extent/avgextent)):
                    pyautogui.click(x = c[0] + i * avgextent, y= c[1] + j * avgextent)
