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

file_list = ['REG-F-RS101 Signed Status Report Comparison',
		'REG-F-RS102 Depart Status Report Comparison',
		'REG-F-RS103 Return Status Report Comparison',
		'REG-F-RS104 Approved Status Report Comparison',
		'REG-F-RS105 Traveler Status Report Comparison',
		'REG-F-RS106 Adjustment Report Comparison',
		'REG-F-RS107 Routing Status Report Comparison',
		'REG-F-RS109 Unsubmitted Voucher Report Comparison',
		'REG-F-RS110 CBA TO Report Comparison',
		'REG-F-RS111 Debt Management Report Comparison',
		'REG-F-RS112 Constructed Travel Report Comparison',
		'REG-F-RS113 FPLP FEMA Report Comparison',
		'REG-F-RS114 Reason Code Report Comparison',
		'REG-F-RS115 Reason Justification Report Comparison',
		'REG-F-RS118 Enlisted BAS Report Comparison',
		'REG-F-RS119 FSA Report Comparison',
		'REG-F-RS120 Special Duty Report Comparison',
		'REG-F-RS121 Military Leave Report Comparison']

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
		result_str = '\nFile not found in\n' + file_path
		result_logger.write(result_str)
		result_logger.close()
		return False

# CURRENTLY NOT WORKING
def findColumnDiff(before_list, after_list):
	"""
	The function checks two lists of strings and find all the columns
	that contain differences and returns the list of difference
	"""
	diff_list = []

	# in case the two lists have different lengths
	if len(before_list) <= len(after_list):
		list_length = len(before_list)
	else:
		list_length = len(after_list)

	for idx in range(list_length):
		if not(before_list[idx] == after_list[idx]):
			diff_list.append(idx)
	
	return diff_list

def checkLineDiff(before_file, after_file, result_file):
	"""
	The function checks the files specified by the parameters and returns
	True if the file contents match, returns False if there is mismatch
	and writes the location of the difference in the result log in
	result_log
	"""
	file_before = open(before_file, 'r')
	file_after = open(after_file, 'r')
	# parse the contents
	before_content = list(file_before)
	after_content = list(file_after)

	before_length = len(before_content)
	after_length = len(after_content)

	# the result log file
	result_writer = open(result_file, 'a')

	# compare the content
	if before_length == after_length:
		all_matched = True
		for idx in range(2, before_length):
			if not(before_content[idx] == after_content[idx]):
				# flip the match flag
				all_matched = False

				mismatch_str = '\nMismatch at line '
				temp_str = str(idx + 1)
				mismatch_str += temp_str
				result_writer.write(mismatch_str)
				
		if all_matched:
			result_writer.write('\nAll data matched')
	else:
		all_matched = False
		# content length mismatched
		result_writer.write('\nFiles\' content volumes mismatched')

	# close the files
	file_before.close()
	file_after.close()
	result_writer.close()

	return all_matched

# Main body
# create log file
result_log_path = general_path + result_file + result_file_format
result_log = open(result_log_path, 'w')
result_log.close()

for file_name in file_list:
	before_path = general_path + before_str + file_name + file_format
	after_path = general_path + after_str + file_name + file_format
	
	# check if files exist
	if checkFileExists(before_path, result_log_path) and\
	checkFileExists(after_path, result_log_path):
		result_log = open(result_log_path, 'a')
		result_log.write('\n' + file_name)
		matching = checkLineDiff(before_path, after_path, result_log_path)
		if matching:
			result_log.write('\nAll data matched')
		result_log.close()

print('finished')

