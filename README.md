# Usage
Find and click all targets in the (hard-coded) cropped region to remove the HUD and toolbelt on a fullscreen 1080p display at 100% UI scale:

`sleep 10 && /usr/bin/python3 vaporize.py`

This will immediately take a screenshot and click everything red within the cropped region. Collision detection is done based on average red target size so as to conserve ammunition. Targets are sorted by distance from the mouse position when the program is invoked. Use a program like `xpad` (think sticky notes or masking tape) to mask off parts of the screen that you don't want shot. `sleep` is used to give time to move from console to `factorio` and equip the artillery remote control. Alternately, you may keybind your window manager to execute the script. It can also be helpful to bind another key combination to kill the process if your birrage goes awry or if you want to give the biters (or your defenses) a break.

# Requirements

`pip3 install pyautogui`

If you need to use a different crop region, you can change the first couple of lines of the pyautogui screenshot command.

Please feel free to ask questions! 

# Warranty
Don't shoot your own guns and trains! It clicks red regardless of force. It will click custom UI elements as well. 

Buyer beware!!!
