import string

def findIndex(the_file, the_option):

	charInOption = len(the_option)	#number of characters in the option string
	# verify the number of times the option appears
	occurrence = the_file.count(the_option)
	#print occurrence

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

	return the_index

def replaceFunc(the_file, the_option, start, stop, switchIt):
	
	#charInOption = len(the_option)
	#start2 = start + charInOption +1	#after the option and '=' sign
	
	if  start2 < stop:
		
	else:
		exit(0)