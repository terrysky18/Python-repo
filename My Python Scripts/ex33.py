def build_list(*args):
	index = 0
	numbers = []

	while index < eleNum:
		print "At the top i is %d" % i
		numbers.append(index)
	
		index+=1
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i
	
	return numbers

the_List = build_list(int(howMany))	#howMany is a string, so it needs to be cast as an int

print "The numbers: "

for num in the_List:
	print num
