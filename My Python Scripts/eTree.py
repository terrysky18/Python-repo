import xml.etree.ElementTree as ET
from sys import argv
script, version = argv

build_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

file_loc = build_loc + "\preferences.xml"

#Parse the XML and get the root element
tree = ET.parse(file_loc)
root = tree.getroot()

#Recursively search all children of the root looking for what we want to change
for attribute in root.iter('user_modifiable'):
	new_value = 'true'
	attribute.text = 'true'

tree.write(file_loc)
