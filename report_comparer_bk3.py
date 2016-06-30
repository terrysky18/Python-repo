"""
A script that compares two sets of csv files and checks for differences
writes the comparison results to a text file
"""

import csv
import os.path

# General Information
# This section contains directory and file information
general_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\'

before_str = 'before\\'
after_str = 'after\\'

# the word Comparison is removed to avoid confusion
file_list = ['REG-F-RS101 Signed Status Report',
		'REG-F-RS102 Depart Status Report',
		'REG-F-RS103 Return Status Report',
		'REG-F-RS104 Approved Status Report',
		'REG-F-RS105 Traveller Status Report',
		'REG-F-RS106 Adjustment Report',
		'REG-F-RS107 Routing Status Report',
		'REG-F-RS109 Unsubmitted Voucher Report',
		'REG-F-RS110 CBA TO Report',
		'REG-F-RS111 Debt Management Report',
		'REG-F-RS112 Constructed Travel Report',
		'REG-F-RS113 FPLP FEMA Report',
		'REG-F-RS114 Reason Code Report',
		'REG-F-RS115 Reason Justification Report',
		'REG-F-RS118 Enlisted BAS Report',
		'REG-F-RS119 FSA Report',
		'REG-F-RS120 Special Duty Report',
		'REG-F-RS121 Military Leave Report']

before_end = ' before'
after_end = ' after'
file_format = '.csv'

# result file information
result_file = 'DOCSTAT comparison result'
result_file_format = '.txt'

# Functions
def checkFileExists(file_path, result_path):
	"""
	The function checks whether the file specified by file_path exist;
	returns True if the file exists, return False if the file isn't
	found and logs the result to result file in result_path
	"""
	if os.path.isfile(file_path):
		# file found
		return True
	else:
		# file not found
		result_logger = open(result_path, 'a')
		result_str = '\nFile not found in\n' + file_path + '\n'
		result_logger.write(result_str)
		result_logger.close()
		return False


def findColumnDiff(before_list, after_list):
	"""
	The function checks two list of strings and finds all the columns
	that contains differences and returns the list of difference
	"""
	diff_list = []
	
	if len(before_list) <= len(after_list):
		list_len = len(before_list)
	else:
		list_len = len(after_list)
	#list_len = len(before_list)
	for idx in range(list_len):
		if not(before_list[idx] == after_list[idx]):
			diff_list.append(idx)
	return diff_list


def checkLineDiff(before_file, after_file):
	"""
	The function checks the files specified by the parameters and returns
	a result string for writing to the result log file
	"""
	file_before = open(before_file, 'r')
	file_after = open(after_file, 'r')
	# parse the contents
	before_content = list(file_before)
	after_content = list(file_after)

	before_length = len(before_content)
	after_length = len(after_content)

	result_str = ''
	# compare the content
	if before_length == after_length:
		all_matched = True
		for idx in range(6, before_length):
			# split the comma delimited string into a list
			before_entry = before_content[idx].split(',')
			after_entry = after_content[idx].split(',')
			
			if not(before_entry == after_entry):
				# flip the match flag
				all_matched = False
				
				# write line containing difference
				mismatch_str = '\nMismatch at line '
				temp_str = str(idx + 1)
				mismatch_str += temp_str

				# write out the difference
				# list of indices
				diff_idx = findColumnDiff(before_entry, after_entry)
				temp_str = ''
				for jdx in diff_idx:
					temp_list = before_content[5].split(',')
					temp_str += '\n' + temp_list[jdx]
					temp_str += '\nbefore: ' + before_entry[jdx]
					temp_str += '\nafter: ' + after_entry[jdx]
				mismatch_str += temp_str + '\n'
				result_str += mismatch_str

		if all_matched:
			result_str = '\nAll data matched'
	else:
		# content length mismatched
		result_str = '\nFile content volumes mismatched'

	# close the files
	file_before.close()
	file_after.close()

	return result_str

# Main body
# create log file
result_log_path = general_path + result_file + result_file_format
result_log = open(result_log_path, 'w')
result_log.close()

for file_name in file_list:
	before_path = general_path + before_str + file_name + before_end + file_format
	after_path = general_path + after_str + file_name + after_end + file_format

	# check if files exist
	if checkFileExists(before_path, result_log_path) and\
	checkFileExists(after_path, result_log_path):
		result_log = open(result_log_path, 'a')
		result_log.write(file_name)
		logging = checkLineDiff(before_path, after_path)
		result_log.write(logging + '\n\n')
		result_log.close()

print('finished')

