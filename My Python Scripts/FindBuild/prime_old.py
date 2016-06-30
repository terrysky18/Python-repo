from os import listdir
from os.path import isfile, join
from os.path import getmtime
import datetime
import argparse


#Provide a description the programme

autobot = argparse.ArgumentParser(description="automate the process of receiving the latest build and changing different setting")

#positional argument, specify either Enterprise or Dell, default is Enterprise
# nargs='?' makes 'release' an optional positional argument

autobot.add_argument("release", nargs='?', default="Enterprise",
		help="specify the product, Invincea Enterprise or Dell protected workspace")

#optional argument, specify the build number, default is latest

autobot.add_argument("-b", "--build", default="latest",
		help="specify the build number")

#optional argument, checks and return the build number of the latest build

autobot.add_argument("-l", "--latest", action="store_true", default=None,
		help="check for the latest build kit via time stamp")

OpPrime = autobot.parse_args()	# parses all arguments


def FileList(the_path, release=None):

	files = []
	index = 0	# index for checking file list
	tempfiles = listdir(the_path)

	endList = len(tempfiles) # length of the file list

	while index < endList:  # build the list of all installer kit
		if isfile(join(the_path, tempfiles[index])):
		# isfile() requires the full directory of the file, join is needed
			files.append(tempfiles[index])
			# .append() adds the element to back of the list

		index+=1
		#end while loop

	if (release is None):	# no release is specified
		return files	# all installer kit included

	else:		# either Enterprise or Dell is specified
		filtered = []
		index = 0
		endList = len(files)

		while index < endList:  # build the list specific installer kit
			if release.lower() in files[index].lower():
			# calls .lower() to eliminate case sensitivity
			# checks if enterprise or dell in the installer names
				filtered.append(files[index])
			else:
				pass	# no alternative action needed

			index+=1
			#end while loop

		return filtered	# only kit specified by release are included

	#end of FileList() definition

def GetLatestFile(the_path, file_list):
# find the latest build file by comparing modified time in files from file_list
# then returns the latest build file

	index = 0
	endList = len(file_list)

	t = getmtime(join(the_path, file_list[index])) # initial value
	latestFile = file_list[index]	# initial value for comparison

	while index < endList:
		new = getmtime(join(the_path, file_list[index]))

		if t < new:
			t = new
			latestFile = file_list[index]
		else:
			pass

		index+=1
		#end while loop
	
	return latestFile

	#end of GetLatestFile() definition

def GetSpecificBuild(the_path, file_list, the_build):
# the function is used when a specific build is requested

	index = 0
	endList = len(file_list)
	requestedBuild = 'invald'	# initial value for checking

	while index < endList:
		if the_build not in file_list[index]:
			pass	# when build isn't found keep searching
		else:	# found build
			requestedBuild = file_list

		index+=1
		#end while loop
	
	if 'invalid' not in requestedBuild:
		return requestedBuild
	else:
		print "Build not found"
		return requestedBuild

	#end of GetSpecificBuild() definition

def ShowFileInfo(the_path, the_file):
# void type function, prints modified time of the parameter the_file

	tStamp = getmtime(join(the_path, the_file))

	# use datetime.fromtimestamp to convert time stamp into readable form
	print datetime.datetime.fromtimestamp(tStamp)

	#end of ShowFileInfo() definition

def main():

	#file_path = r"\\beaver\Builds"
	file_path = r"C:\Users\terry.song\Desktop\build folder script test"

	if "latest" not in OpPrime.build:  # -b is invoked, specific build requested
		installerFiles = FileList(file_path, OpPrime.release)

		desiredFile = GetSpecificBuild(file_path, installerFiles, OpPrime.build)
		if 'invalid' in desiredFile:
			break
		else:
			print desiredFile

	else:
		desiredFile = GetLatestFile(file_path, installerFiles)

		if OpPrime.latest:  # -l is invoked, the script shows the latest build
			print desiredFile
			ShowFileInfo(file_path, desiredFile)
		else:
			pass

	#end of main() definition

if __name__ == "__main__":
	main()

