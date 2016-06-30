import win32gui
import time

tempWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
print tempWindowName

while True:
	if (tempWindowName == win32gui.GetWindowText(win32gui.GetForegroundWindow())):
		pass
	else:
		tempWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
		print tempWindowName
	
	time.sleep(0.1)
