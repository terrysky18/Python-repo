# Outdated method
# Module to copy the content of a preferences to a preferences in a build folder
import sys

def theCopier(build_loc):
	#location of the build preferences.xml
	file_loc = build_loc + "\preferences.xml"
	
	#location of the source preferences.xml
	sourceLoc = "C:\Users\\terry.song\Documents\invincea enterprise documentation\preferences.xml"
	
	#read the content of the source file
	in_file = open(sourceLoc)
	indata = in_file.read()
	
	#write the source file content to the target file
	out_file = open(file_loc, 'w')
	out_file.truncate()		#erase the original content
	out_file.write(indata)
	
	#close the files
	out_file.close()
	in_file.close()
