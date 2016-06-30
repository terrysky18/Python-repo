# A script to try to use the shutil module functions

import os
import shutil
from sys import argv

script, version = argv	#ask for the build version number when the script is executed
#location of the build
src_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

dst_loc = "C:\Users\\terry.song\Desktop\\backup InvinceaEnterprise_" + version

shutil.copytree(src_loc, dst_loc)
