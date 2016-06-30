from sys import argv
import string

script, version = argv

#location of the build
build_loc = "C:\Users\\terry.song\Desktop\InvinceaEnterprise_" + version

file_loc = build_loc + "\preferences.xml"

the_file = open(file_loc).read()
#print the_file

the_option = 'user_modifiable'	#the option in the preferences.xml
charInOption = len(the_option)	#number of characters in the option string
# verify the number of times the option appears
occurrence = the_file.count(the_option)
print occurrence

# total number of characters in the file
totalChar = len(the_file)
print totalChar
#print the_file[totalChar-1]

index = 0
the_index = []

while index < occurrence:
	if index > 0:
		the_index.append(index)		#add an element to the list
		the_index[index] = the_file.find(the_option, the_index[index-1]+charInOption, totalChar-1)
	else:	#first time
		the_index.append(index)		#add an element to the list
		the_index[index] = the_file.find(the_option)
	
	index += 1
	#print the_file[0:(the_index+1)]

print the_index
