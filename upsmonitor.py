#!/usr/bin/env python3

import math
import pyautogui

import random
from PIL import Image

import pytesseract
import numpy as np
import cv2

pyautogui.PAUSE = 0.5

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
upsx1 = 1459
upsx2 = 1656
#upsy1 = 12
#upsy2 = 36
upsy1 = 28
upsy2 = 56
ups = ss.crop((upsx1, upsy1, upsx2, upsy2))

for x in range(ups.width): 
    for y in range(ups.height): 
        p = ups.getpixel((x,y))
        if p[0] > 128 and p[1] > 128 and p[2] > 128:
            ups.putpixel((x,y), (255,255,255,255))
        else:
            ups.putpixel((x,y), (0,0,0,0))

ups = np.asarray(ups)
ups = cv2.GaussianBlur(ups, (1,1), 0)
#ups = cv2.threshold(ups, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#ups = cv2.morphologyEx(ups, cv2.MORPH_OPEN, kernel, iterations=1)
ups = (255-ups)

ups = Image.fromarray(ups)
ups.save('snippet.jpg')

text = pytesseract.image_to_string(ups, config='--psm 6').strip()
print(text)
with open('ups.txt', "w") as f: f.write(text)
