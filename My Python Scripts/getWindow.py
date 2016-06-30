# This script prints out all the windows currently exist in a Windows session
# Some windows are hidden and users are not able to see and interact with them

import win32gui
import win32con

toplist = []
winlist = []

def enum_callback(hwnd, results):
	winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

win32gui.EnumWindows(enum_callback, toplist)
toplist = [(hwnd) for hwnd in winlist]# if 'python' in title.lower()]
#grab the first window that matches
print toplist
