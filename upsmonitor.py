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
upsx1 = 1465
upsx2 = 1655
#upsy1 = 12
#upsy2 = 36
upsy1 = 24
upsy2 = 50
ups = ss.crop((upsx1, upsy1, upsx2, upsy2))

ups.save('snippet.jpg')
text = pytesseract.image_to_string(ups).strip()
with open('ups.txt', "w") as f: f.write(text)
