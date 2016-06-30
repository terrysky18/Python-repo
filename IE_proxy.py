"""
Internet Explorer 8 proxy setting is lost after every reboot
This script helps restoring the setting and ease the user's
need to reenter the setting before using IE8
"""
from sys import argv
from Tkinter import Tk

script, proxy_select = argv

def make_string(string_list):
	result_string = ''
	for elem in string_list:
		result_string += elem
		result_string += ';'
	return result_string

proxy_exceptions = ['12.154.90.*', '192.168.*', '214.3.110.*',
		'214.10.12.*', '*.defensetravel.osd.mil', '*.govtrip.com',
		'*.northropgrumman.com', '*.sabre.com', '*.wspan.com',
		'*.worldspan.com', '*.northgrum.com', '*.northrop.com',
		'*.grumman.com']
proxy_server = 'contractorproxy.ms.northgrum.com'

if proxy_select == '1':
	be_copied = proxy_server
elif proxy_select == '2':
	be_copied = make_string(proxy_exceptions)

# copy string to Windows clipboard
copier = Tk()
copier.withdraw()
copier.clipboard_clear()
copier.clipboard_append(be_copied)
copier.destroy()
