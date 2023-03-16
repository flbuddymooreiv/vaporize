# Usage
Find and click all targets in the middle 60% of the screen. When the script starts, it will outline the region by moving the mouse pointer to the corners in a clockwise
fashion such that a preview of the search space is visualized. It is beneficial to
set up a hotkey or an emergency kill command such as follows:

`pkill -if 'python.*vaporize'`

This will immediately take a screenshot and click everything red within the cropped region. Collision detection is done based on average red target size so as to conserve ammunition. Targets are sorted by distance from the mouse position when the program is invoked. Use a program like `xpad` (think sticky notes or masking tape) to mask off parts of the screen that you don't want shot. `sleep` is used to give time to move from console to `factorio` and equip the artillery remote control. Alternately, you may keybind your window manager to execute the script. It can also be helpful to bind another key combination to kill the process if your birrage goes awry or if you want to give the biters (or your defenses) a break.

# Requirements

`pip3 install pyautogui`

`pip3 install pytesseract`

`pip3 install numpy`

`pip3 install opencv-python`

`pip3 install pillow`

`sudo apt-get install scrot`

# Warranty
Don't shoot your own guns and trains! It clicks red regardless of force. It will click custom UI elements as well. 

Buyer beware!!!

# Enjoy
Do it. Spare you mouse.
