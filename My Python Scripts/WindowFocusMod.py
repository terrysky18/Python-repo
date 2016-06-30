import win32gui
import win32con

toplist = []
winlist = []

def _enum_callback_(hwnd, results):
	winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def ManoeuvreWindow(windowTitle, control):
# Sets focus on the window or minimise the window specified by the windowTitle
# windowTitle is the name of the window, must be a string variable
# control is the option to manoeuvre the window, 'm' for minimise, 'f' for set focus

	if isinstance(windowTitle, str) and isinstance(control, str):
		win32gui.EnumWindows(_enum_callback_, toplist)
		targetWindow = [(hwnd, title) for hwnd, title in winlist if windowTitle in title.lower()]
		#grab the first window that matches
		target = targetWindow[0]

		if control == 'f':
			#use the window handle to set focus
			win32gui.SetForegroundWindow(target[0])
			
		elif control == 'm':
			#minimise the window
			win32gui.ShowWindow(target[0], win32con.SW_MINIMIZE)

	else:
		print 'parameter must be a string variable'
