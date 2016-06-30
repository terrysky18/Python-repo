import os.path
import sys
import csv
import math		# for using trigonometric functions

# Define my own range() function that accomondates decimals
def decRange(start, stop, step):
	list = [start]
	newElem = start		#next element to add to the array
	
	while newElem < stop:	#as long as the next element is less than or equal to stop
		newElem += step
		list.extend([newElem])
	
	return list

x = decRange (0, 2*math.pi, 0.01)
print len(x)

