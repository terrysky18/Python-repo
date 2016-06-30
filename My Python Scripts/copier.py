import os
import shutil
import fnmatch
from sys import argv

#script, version = argv	#ask for the build version number when the script is executed

directory = '\\' + '\\beaver\\Builds'	#product build location

#search pattern
product1 = 'InvinceaEnterprise_*'
product2 = 'DellSetup_*'

excludes = [product1 + '\\']
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

for root, dirs, files in os.walk(directory):

	for filename in fnmatch.filter(files, product1):
		print os.path.join(root, filename)

# theBuild = product1 + version
# src_loc = os.path.join(directory, theBuild)

# if os.path.exists(src_loc):
	# dst_loc = "C:\Users\\terry.song\Desktop\\backup " + theBuild
	# shutil.copytree(src_loc, dst_loc)
	# print 'Completed'
	
# else:
	# print 'File path invalid'
	# exit(0)
