# An example file to show the capability of Mouse class

import time
from Mouse import Mouse

mouse = Mouse()
mouse.move_mouse((0, 0))
mouse.click((20, 10), "right")
time.sleep(1.5)
mouse.click((30, 20), "left")
