from Xlib import display
import os
from pybeep.pybeep import PyVibrate, PyBeep

beep = lambda x: os.system("beep -f 555 -l 460")
while True:
    data = display.Display().screen().root.query_pointer()._data
    print(data["root_x"], data["root_y"])
    if data["root_x"] == 0 and data["root_y"] == 0:
        beep(3)
