import time
from os import path

def createFile(dest):
	"""
	The script creates a text file at the passed in location,
	names file based on date
	"""
	date = time.localtime(time.time())
	## FileName: Year_Month_Day
	name = '%d_%d_%d.txt' %(date[0], date[1], date[2])

	if not (path.isfile(dest + name)):
		# check if file exist
		f = open(dest + name, 'w')
		f.write('\n' * 30)
		f.close()


if __name__ == '__main__':
	destination = r"C:\Users\terry.song\Documents\My Python Scripts\LearnMkFile\\"
	createFile(destination)
	raw_input('done')

