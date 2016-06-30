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

def checkLineDiff(before_file, after_file):
	"""
	The function checks the files specified by the parameters and returns
	a result string for writing to the result log file
	"""
	file_before = open(before_file, 'r')
	file_after = open(after_file, 'r')
	
	# read the files
	before_reader = csv.reader(file_before)
	after_reader = csv.reader(file_after)
	
	# parse the contents
	before_content = list(before_reader)
	after_content = list(after_reader)

	before_length = len(before_content)
	after_length = len(after_content)

	result_str = ''
	# compare the content
	if before_length == after_length:
		# content lengths match
		all_matched = True
		for idx in range(3, 6):
			print(before_content[idx], after_content[idx])

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
