import ctypes

# EnumWindows: enumerate all top level windows
EnumWindows = ctypes.windll.user32.EnumWindows

# EnumWindowsProc: callback function will be called for each top most window
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

# GetWindowText: get the window titles
GetWindowText = ctypes.windll.user32.GetWindowTextW

# GetWindowTextLength: get the right buffer size to hold the string
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW

# IsWindowVisible: filter the windows to weed out not useful information
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []

def foreach_window(hwnd, lParam):
	if IsWindowVisible(hwnd):
		length = GetWindowTextLength(hwnd)
		buff = ctypes.create_unicode_buffer(length + 1)
		GetWindowText(hwnd, buff, length + 1)
		titles.append(buff.value)
	return True

def main():
	EnumWindows(EnumWindowsProc(foreach_window), 0)

if __name__=='__main__':
	main()
	print titles
