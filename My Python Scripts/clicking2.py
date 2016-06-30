# A script to try how to use python to position the mouse

import ctypes
import time

ctypes.windll.user32.SetCursorPos(1, 0)
time.sleep(3)

ctypes.windll.user32.SetCursorPos(960, 0)
time.sleep(3)

ctypes.windll.user32.SetCursorPos(1920, 0)
time.sleep(3)
