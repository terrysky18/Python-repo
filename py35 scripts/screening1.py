def printSymbol(num):
	"""
	Print the pound symbol '#' in the following pattern
	#
	##
	###
	####
	###
	##
	#
	param:  num - the maximum number of # printed
	return:  void
	"""
	if num > 0:
		repeat = 1
		pattern = ""
		# Print the upper half
		while (repeat <= num):
			for i in range(repeat):
				pattern += "#"
			print(pattern)
			pattern = ""
			repeat += 1

		# Print the lower half
		repeat -= 2	# repeat is greater than num by 1
		while (repeat >= 1):
			for i in range(repeat):
				pattern += "#"
			print(pattern)
			pattern = ""
			repeat -= 1

	else:
		print("Parameter cannot be less than 1")


if __name__ == "__main__":
	"""
	Demonstration of the script
	"""
	printSymbol(4)
	print("\n")
	printSymbol(6)
	printSymbol(0)
