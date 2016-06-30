# The script takes the build revision number and copies build packet to desktop
# like an autonomous robot, autobot

import os
import shutil
from sys import argv
import PrepFilesmod as prep

script, version = argv	#ask for the build version number when the script is executed

#source and destination for the build
srcLoc = '\\\\beaver\\Builds\\InvinceaEnterprise_' + version
dstLoc = 'C:\\Users\\terry.song\\Desktop\\InvinceaEnterprise_' + version

# check if the build packet is already on desktop
if not(os.path.exists(dstLoc)):
	if os.path.exists(srcLoc):
		#copy the build installer packet to desktop
		shutil.copytree(srcLoc, dstLoc)
	else:
		print 'Build packet directory invalid'
		exit(0)
else:
	print 'Build folder already exists in destination directory'
	carryOn = raw_input('Continue to modify the packet (Y/N)?: ')
	
	if carryOn.lower() == 'n':
		exit(0)

prep.keyChanger(dstLoc, 1)		#put in the activation key for test
prep.UserModifiableOnOff(dstLoc, 1)		#turn on all user modifiable options
prep.FunctionOnOff(dstLoc, 'software_update', 0)	#turn off software update function
prep.FunctionOnOff(dstLoc, 'office_protection', 1)	#turn on office protection
# prep.AddNewFunction(dstLoc, 'Chrome', 1)	#enable google chrome support

print "Completed"

os.startfile(dstLoc + '\\activationkey.txt')
os.startfile(dstLoc + '\\preferences.xml')
