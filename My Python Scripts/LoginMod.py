import VirtualKeyboard as vk
import time
import subprocess
import win32gui

def _login_():
	usrnm = r'invincea.local\terry.song'
	pswrd = r'$ky2oo2!18'
	
	print 'autonomous log in'
	time.sleep(0.5)
	vk.typer(usrnm)
	vk.press('tab')
	vk.typer(pswrd)
	vk.press('enter')

def OpenFolder(folderName, close=None):
# Opens a network folder, automatically logs in the network to allow file transfer
# 
	subprocess.Popen(r'explorer ' + folderName)
	time.sleep(2)	# wait for the explorer window to appear
	WindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
	
	if 'Connect to' in WindowName:
		_login_()

	if 'c' in close:
		time.sleep(0.5)
		vk.pressAndHold('ctrl')
		vk.press('w')
		vk.release('ctrl')
