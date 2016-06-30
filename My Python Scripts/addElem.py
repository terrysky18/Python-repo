import xml.etree.ElementTree as ET

thefile = 'preferences.xml'
fileTree = ET.parse(thefile)
fileRoot = fileTree.getroot()

newNodeStr = 'Chrome'

sigma = len(fileRoot)
print sigma

tag = ET.tostring(fileRoot[0])	#cast the tag to string
print newNodeStr not in tag		#compare the existing tag to 

for element in fileRoot:
	tag = ET.tostring(element)
	
	if newNodeStr in tag:
		print 'match'

print fileRoot[sigma-1]
