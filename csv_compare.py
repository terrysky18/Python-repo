"""
A simple script to compare two sets of csv files and write the results
out to a text file
"""

import csv

general_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\'

before_file = 'REG-F-RS101 Signed Status Report Comparison'
after_file = 'REG-F-RS101 Signed Status Report after.csv'
result_file = 'comparison result.txt'

# open the files
before_open = open(general_path + before_file + '.csv', 'r')
after_open = open(general_path + after_file, 'r')
result_writer = open(general_path + result_file, 'w')

# read the files
before_reader = csv.reader(before_open)
after_reader = csv.reader(after_open)
#before_reader = csv.reader(open(general_path+before_file+'.csv', 'r'))
#after_reader = csv.reader(open(general_path+before_file+'.csv', 'r'))

# parse the contents
before_content = list(before_reader)
after_content = list(after_reader)

# compare the contents
before_length = len(before_content)
after_length = len(after_content)

def findColumnDiff(before_list, after_list):
	diff_list = []
	#print(len(before_list))
	#print(len(after_list))
	
	for idx in range(len(before_list)):
		if not(before_list[idx] == after_list[idx]):
			diff_list.append(idx)
	return diff_list

if not(before_length == after_length):
	result_writer.write('File content volumes mismatched')
else:
	result_writer.write(before_file)
	for idx in range(2, before_length):
		print(type(before_content[idx]))
		if not(before_content[idx] == after_content[idx]):
			mismatch_str = '\nMismatch at line '
			temp_str = str(idx + 1)
			mismatch_str += temp_str
			result_writer.write(mismatch_str)
			diff_idx = findColumnDiff(before_content[idx], after_content[idx])
			temp_str = ''
			for jdx in diff_idx:
				temp_str += '\n' + before_content[5][jdx]
				temp_str += '\nbefore: ' + before_content[idx][jdx]
				temp_str += '\nafter: ' + after_content[idx][jdx]
			result_writer.write(temp_str)

	result_str = '\nAll data matched'

# finish processing, close files
before_open.close()
after_open.close()
result_writer.close()

