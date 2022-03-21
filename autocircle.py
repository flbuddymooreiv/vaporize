#!/usr/bin/env python3

import math
import pyautogui

pyautogui.PAUSE = 0.01

def loop(heading):
    #pos = pyautogui.mouseinfo.position()
    x = 5 * math.sin(heading)
    y = 5 * math.cos(heading)

    print(x,y)
    pyautogui.moveRel(x,y)
    pyautogui.click()

heading = 0
while True:
    heading += .3
    loop(heading)
