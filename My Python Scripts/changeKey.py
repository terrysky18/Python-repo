from sys import argv
import PrepFilesmod as prep
import os as operator
import shutil as copier

script, version = argv	#ask for the build version number when the script is executed

# location of the build
build_loc = "C:\\Users\\terry.song\\Desktop\\InvinceaFreespace_Kit_" + version

# modify the preference.xml file
prep.keyChanger(build_loc, 1)
prep.UserModifiableOnOff(build_loc, 1)
prep.FunctionOnOff(build_loc, 'software_update', 1)
prep.FunctionOnOff(build_loc, 'web_redirector', 1)
prep.FunctionOnOff(build_loc, 'office_protection', 0)
prep.FunctionOnOff(build_loc, 'show_border', 0)
prep.FunctionOnOff(build_loc, 'kill_suspected_processes', 1)

prep.FunctionModify(build_loc, 'config_server', 'server', 'http://10.9.8.134:443/api')
prep.FunctionModify(build_loc, 'report', 'address', 'http://10.9.12.134:443')
prep.FunctionModify(build_loc, 'autorestore', 'randomize_minutes', '0')

# get to the new custom_apps.xml to allow extensions
#operator.remove(build_loc + '\\custom_apps.xml')

#copier.copyfile("C:\\Users\\terry.song\\Desktop\\custom_apps (whitelisted).xml", build_loc + '\\custom_apps.xml')

print "Completed"