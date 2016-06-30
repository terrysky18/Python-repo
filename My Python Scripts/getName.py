# The script displays the registered name of the account
# changing the NameDisplay value changes the name being printed

import ctypes

def get_display_name():

	# declaration for GetUserNameEx
	GetUserNameEx = ctypes.windll.secur32.GetUserNameExW	#GetUserNameExW is the unicode W (wide) version
	
	# GetUserNameEx takes an EXTENDED_NAME_FORMAT, a friendly display name 3
	NameDisplay = 3
	
	size = ctypes.pointer(ctypes.c_ulong(0))
	GetUserNameEx(NameDisplay, None, size)
	
	nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
	GetUserNameEx(NameDisplay, nameBuffer, size)
	return nameBuffer.value

if __name__ == "__main__":
	print get_display_name()
