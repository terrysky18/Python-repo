# A script to show how to use python to control the mouse

import ctypes
import time

# drag the mouse the creat a retangle
ctypes.windll.user32.SetCursorPos(500, 80)
ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)	# left button down
ctypes.windll.user32.SetCursorPos(850, 180)

time.sleep(3)		# pause 3 seconds
ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)	# left button up

#ctypes.windll.user32.SetCursorPos(500, 100)
