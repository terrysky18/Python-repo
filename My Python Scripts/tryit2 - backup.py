import xml.etree.ElementTree as ET
from sys import argv
script, version = argv

def checkContent(root, writeOut):
	# write the parsed xml to text file for visual inspection
	if writeOut > 0:
		output_file = build_loc + '\\theOutput.txt'
		target = open(output_file, 'w')
		target.truncate()
	
	i = 0
	the_tags = []
	theAttributes = []

	for child in root:
		the_tags.append(i)
		the_tags[i] = child.tag
		
		theAttributes.append(i)
		theAttributes[i] = child.attrib
		
		i +=1
	
		if writeOut > 0:
			target.write(child.tag)
			attribute = '  ' + str(child.attrib)
			target.write(attribute)
			target.write('\n')

	if writeOut >0:
		target.close()
	
	return (the_tags, theAttributes)

#location of the build
build_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

file_loc = build_loc + "\preferences.xml"

#read the xml file from a defined location
file_tree = ET.parse(file_loc)
file_root = file_tree.getroot()

results = checkContent(file_root, 0)
Tags = results[0]
Attributes = results[1]

if len(Tags)!=len(Attributes):	#tags and attributes entries don't match
	print 'Something is wrong with the preferences.xml file'
	exit(0)

numLines = len(Tags)
the_option = 'user_modifiable'	#the option in the preferences.xml

i = 0
while i < numLines:
	if the_option in Attributes[i]:
		
		print Tags[i]
		print Attributes[i]
		
	i +=1
	
file_tree.write(file_loc)
