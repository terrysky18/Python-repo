from sys import argv
import string
import PrepFilesmod

script, version = argv

#location of the build
build_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

file_loc = build_loc + "\preferences.xml"

the_file = open(file_loc).read()
the_option = 'user_modifiable'	#the option in the preferences.xml

theIndice = PrepFilesmod.findIndex(the_file, the_option)
print theIndice
print the_file[theIndice[0]:theIndice[1]]

occurrence = the_file.count(the_option)
