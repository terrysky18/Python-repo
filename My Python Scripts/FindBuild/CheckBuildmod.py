import os
import sys
import time
import datetime

# The main body that runs the module file as a script
def main():
	version = raw_input('version: ')
	filePath = 'C:\\Users\\terry.song\\Desktop\\InvinceaEnterprise_Kit_' + version + '.exe'

	#get the modified time of the file
	tmodifiedTime = os.path.getmtime(filePath)  #floating point value
	modifiedTime = datetime.datetime.fromtimestamp(tmodifiedTime)
	
	print modifiedTime

# Allows the module file to run as a script
if __name__ == "__main__":
	main()
