from Mouse import Mouse
import time

mouse = Mouse()
mouse.click((20, 10), "left")
time.sleep(2.0)

mouse.click((100, 100), "right")
