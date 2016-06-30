"""
A script that reads a Debt Management Report and writes the date
out to a new CSV file and converts the date and currency strings
to uniform format
"""
import csv
import re
from datetime import datetime

def checkDate(check_str):
	"""
	check if the parameter string contains a Date
	Return True if the string contains a date
	"""
	# Date pattern
	date_pat = '\d*/\d*/\d*'
	check_obj = re.match(date_pat, check_str)
	return check_obj

def checkCurrency(check_str):
	"""
	check if the parameter string contains a Currency
	Return True if the currency string contains pound or dollar signs
	"""
	currency_pat = '([\$])(\d+(?:\.\d{2})?)'
	check_obj = re.search(currency_pat, check_str)
	return check_obj

def checkNum(check_str):
	"""
	check if the parameter string contains a number
	Return True if the string contains either an int or a float
	"""
	float_pat = '\d*\.\d*'
	int_pat = '^-?[0-9]+$'
	float_obj = re.match(float_pat, check_str)
	int_obj = re.match(int_pat, check_str)
	return float_obj or int_obj

def conStr2DateObj(date_str):
	"""
	converts the parameter string into a date object
	Assumes the string contains a date in format MM/DD/YYYY
	"""
	date_obj = datetime.strptime(date_str, '%m/%d/%Y')
	return date_obj

def conStr2Curren(currency_str):
	"""
	converts the parameter string into a float
	Assumes the string contains a currency
	"""
	value = re.sub(r'[^\d.]', '', currency_str)
	return float(value)

def conStr2Num(num_str):
	"""
	converts the parameter string into a number, int or a float
	Assumes the string contains a number
	"""
	# determine whether an int or a float
	find_obj = re.search('\.', num_str)
	if find_obj:
		# a float
		return float(num_str)
	else:
		# an integer
		return int(num_str)

def writeDiffStr(index, param1, param2, param3, param4=None, param5=None):
	"""
	Takes the parameter strings and generate a
	new string to be written to a log file
	"""
	temp_str = '\n\nMismatch at line '
	temp_str += str(index + 1)
	temp_str += ', ' + param1
	result_str = temp_str
	if param4 and param5:
		temp_str = '\n' + param4 + ' DOCSTAT: ' + param2
		temp_str += '\n' + param5 + ' MView: ' + param3
	else:
		temp_str = '\nDOCSTAT: ' + param2
		temp_str += '\nMView: ' + param3
	result_str += temp_str
	return result_str

"""
Organization
Traveller Last Name
Traveller First Name
Traveller Middle Initial
SSN
TANUM
Document Name
Date Debt Incurred
Date Traveller Notified of Debt
Original Amount of Debt
Last Offset Date
Last Offset Action
Last Offset Amount
Current Balance Due U.S.
Debt Status Flag
Days Since last Activity
Total age of debt in days
Traveller Email Address
DTA ID Email Address
History - Status Type
History - Status Date
History - Transaction Amount
History - Balance Due U.S.
Accountable Station Number
"""
field_names = ['Organization',
				'Traveler Last Name',
				'Traveler First Name',
				'Traveler Middle Initial',
				'SSN',
				'TANUM',
				'Document Name',
				'Date Debt Incurred',
				'Date Traveler Notified of Debt',
				'Original Amount of Debt',
				'Last Offset Date',
				'Last Offset Action',
				'Last Offset Amount',
				'Current Balance Due U.S.',
				'Debt Status Flag',
				'Days Since last Activity',
				'Total age of debt in days',
				'Traveler Email Address',
				'DTA ID Email Address',
				'History - Status Type',
				'History - Status Date',
				'History - Transaction Amount',
				'History - Balance Due U.S.',
				'Accountable Station Number']

# file paths
file_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\'
before_sub = 'before\\retest\\Debt Management (sub) DOCSTAT 7_12.csv'
target_before_sub = 'before\\retest\\Debt MR2 DOCSTAT sub 7_12.csv'

# opening files
source_before = open(file_path + before_sub, 'r')
source_before_reader = csv.reader(source_before)
source_before_read = list(source_before_reader)

target_before = open(file_path + target_before_sub, 'wb')	# open with wb flag to write

# use csv.DictWriter() for writing separate columns
target_before_write = csv.DictWriter(target_before, fieldnames=field_names)

# read the source and write to the target
# DOCSTAT files
for idx in range(5, len(source_before_read)):
	target_dict = {}
	for jdx in range(len(source_before_read[idx])-1):
		#print(source_before_read[idx][jdx])

		if checkDate(source_before_read[idx][jdx]):
			# it's a date string, convert it to uniform format
			date_str = str(conStr2DateObj(source_before_read[idx][jdx]))
			target_str = date_str[:10]	# truncate the time portion
		
		elif checkCurrency(source_before_read[idx][jdx]):
			# it's a currency string, convert it to a floating point number
			target_str = conStr2Curren(source_before_read[idx][jdx])
		
		elif checkNum(source_before_read[idx][jdx]):
			# it's a number string, convert it to a number
			target_str = conStr2Num(source_before_read[idx][jdx])
			
		else:
			# regular string
			target_str = source_before_read[idx][jdx]

		target_dict[field_names[jdx]] = target_str
	target_before_write.writerow(target_dict)

source_before.close()
target_before.close()
print('Finished')
