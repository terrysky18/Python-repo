# The script extracts the contents of a tar.gz file to folder in the current working directory or to a desired directory

import os.path
import sys
import tarfile

script, option, filename = sys.argv
# option can be '-c' to check the content of the file, '-u' to uncompress the file

def Uncompress(file, dst=None):
	if dst is not None:
		file.extractall(dst)	#extract the content to a desired destination
	else:
		file.extractall()		#extract the content to the current directory
	
	print 'Completed'


if os.path.isfile(filename) and tarfile.is_tarfile(filename):	#check to make sure if the file is a tar file
	
	tfile = tarfile.open(filename)	#open the tar file
	
	if 'u' in option:		#'-u' to uncompress the file
		outLoc = raw_input('output location> ')		#ask user for output location
		
		if bool(outLoc):	#the user has entered something
			while True:
				if os.path.exists(outLoc):	#the output path is valid
					Uncompress(tfile, outLoc)
					break
				else:
					outLoc = raw_input('output path invalid, please reenter> ')
		else:
			Uncompress(tfile)
	
	elif 'c' in option:		#'-c' to check the content
		print "\ntar file contents:\n"
		print tfile.list(verbose=False)

else:
	print '\n' + filename + ' is not a valid tar file'
