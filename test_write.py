"""
quick script to practise opening, writing and closing a file
"""

file_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\quick_test.txt'

for dummy_i in range(5):
	write_file = open(file_path, 'w')
	temp = '\nsomething ' + str(dummy_i)
	write_file.write(temp)
	write_file.close()

