from CBAXMLParser import CBAXMLParser
from openpyxl import Workbook
import os.path as path
import DirectoryFileMod as dirFile
import re
import time

def fileCollision(file_name):
	"""
	Appends an appropriate number to the file name when there is file name collision
	The function is called when a collision has been detected
	"""
	dir_file_lst = dirFile.GetFileList()
	match_list = dirFile.CheckFilebyName(file_name, dir_file_lst)
	# append a number to the file name
	new_nm = dirFile.appendNum(file_name, match_list)
	return new_nm

def makeExcelFile(file_name, file_content):
	"""
	Construct an Excel file with name specified by file_name and fill it with information
	contained file_content.  No return type
	file_name is a string
	file_content is an array
	file_content == [account_tag, account_value, transaction_tag]
	"""
	wbook = Workbook()
	# First sheet, Account information
	wsheet1 = wbook.active
	wsheet1.title = "account info"
	wsheet1.append(file_content[0])
	wsheet1.append(file_content[1])

	# Second sheet, Transaction information
	wsheet2 = wbook.create_sheet(title="transactions")
	wsheet2.append(file_content[2])

	for entry in range(xmlParser.GetNumTrans()):
		trans_entry = xmlParser.GetTransVal(entry)
		wsheet2.append(trans_entry)

	wbook.save(out_filename)

def IDfile():
	"""
	Identify the XML file in current directory of the script and return
	name of the file
	"""
	# target file's name begins with ETIC and ends with xml extension
	tgt_str = "^(ETIC)"
	tgt_ext = ".xml"
	
	# list of files in current directory
	cur_dir_file = dirFile.GetFileList()
	# list of xml files in current directory
	xml_files = dirFile.CheckFilebyExt(tgt_ext, cur_dir_file)
	
	if len(xml_files) > 0:
		tgt_list = []
		for file in xml_files:
			file_match = re.search(tgt_str, file)
			if file_match:
				# if file name begins with "ETIC"
				tgt_list.append(file)
		# take the first file in the list
		tgt_file = tgt_list[0]
	else:
		# no XML file found
		print("xml file found in current working directory")
		tgt_file = ""
	return tgt_file


xmlParser = CBAXMLParser()
xml_file = IDfile()
xmlParser.ReadFile(xml_file)

# Parse account information
#account_info = xmlParser.PrintAccountInfo()
account_tag = xmlParser.GetAccountTag()
account_val = xmlParser.GetAccountVal()

# Parse transaction information
#trans_info = xmlParser.PrintTransaction()
trans_tag = xmlParser.GetTransTag()

# Contruct Excel work book
cur_date_str = time.strftime("%Y-%m-%d")
out_filename = "cba_" + cur_date_str + ".xlsx"

if path.exists(out_filename):
	# file already exists
	out_filename = fileCollision(out_filename)

makeExcelFile(out_filename, [account_tag, account_val, trans_tag])
print("XML successfully parsed")
print(out_filename)
time.sleep(1.5)
