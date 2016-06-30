"""
A test script to learn and use the csv module of python to load and read
a csv file
"""

import csv

file_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\REG-F-RS101 Signed Status Report after.csv'

with open(file_path, 'rb') as test_report_file:
	file_reader = csv.reader(test_report_file)
	print(type(file_reader))

	# parse the information from file
	file_content = []
	for row in file_reader:
		file_content.append(row)
	# truncate out useless information
	file_content = file_content[7:]
	print(file_content)

