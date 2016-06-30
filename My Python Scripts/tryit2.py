import xml.etree.ElementTree as ET
from sys import argv
script, version = argv

#location of the build
build_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

file_loc = build_loc + "\preferences.xml"

#read the xml file from a defined location
file_tree = ET.parse(file_loc)
file_root = file_tree.getroot()

the_option = 'user_modifiable'	#the option in the preferences.xml
searchKey = './/*[@' + the_option + ']'

for elem in file_root.iterfind(searchKey):	#search by attribute thanks to XPath support in ElementTree 1.3
	
	elem.set(the_option, 'true')	#

file_tree.write(file_loc)