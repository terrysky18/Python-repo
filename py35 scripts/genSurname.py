"""
A simple script to read from a list of surnames stored in an Excel file and
randomly select a surname to return
"""

import random
import string
from openpyxl import load_workbook

def getName(file_info):
	"""
	The function reads from an Excel file specified in file_info and
	returns the surname saved in the cell.
	The function assumes the names are saved in Sheet1 of the file and
	column A.
	file_info is an array; [file directory, sheet name, column index]
	"""
	file_directory = file_info[0]
	sheet_name = file_info[1]
	col_index = "A"

	temp_idx = file_info[2]
	if type(temp_idx) == int:
		col_index += str(temp_idx)
	else:
		print("Index string is not a number")
		col_index += "1"

	# read the Excel file
	work_book = load_workbook(filename=file_directory)

	if sheet_name in work_book.get_sheet_names():
		sheet_range = work_book[sheet_name]
		the_name = sheet_range[col_index].value
		return the_name
	else:
		# sheet isn't found in file
		print("\nWork sheet not found in Excel work book\n")


def genMultiNames(num_names):
	"""
	The function generates a number of full names specified by the para-
	meter num_names.  The name is presented as surname first then Chris-
	tian name and middle name intitial, such as Walker, John A
	num_names must be an integer
	"""
	middle_init = list(string.ascii_uppercase)
	surnames = "Surnames"
	Christ_names = "Christian names"

	surname_range = 161
	Christ_range = 37

	for idx in range(num_names):
		gen_name = ""
		sur_idx = random.randint(1, surname_range)
		christ_idx = random.randint(1, Christ_range)
		middle_idx = random.randint(1, len(middle_init)) - 1
		gen_name += getName([file_directory, surnames, sur_idx])
		gen_name += ", "
		gen_name += getName([file_directory, Christ_names, christ_idx])
		gen_name += " "
		gen_name += middle_init[middle_idx]
		print(gen_name)


if __name__ == "__main__":
	file_directory = r"C:\Users\jsong\Documents\surname_list.xlsx"

	gen_names = 30
	genMultiNames(gen_names)

