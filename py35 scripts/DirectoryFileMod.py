"""
A module that checks for current working directory for files and file name collisions
"""

import os
import os.path as path
import fnmatch
import re

def _genFileList_(tgt_dir):
	"""
	Generate a list of files in the target directory
	"""
	f_list = [file for file in os.listdir(tgt_dir)
					if path.isfile(path.join(tgt_dir, file))]
	return f_list

def GetFileList(tgt_dir=None):
	"""
	Return a list of files in the directory specified by the parameter.
	If no parameter is received, current working directory is checked
	Folders are excluded from the output.  If the parameter contains
	an invalid directory the output is an empty list.
	"""
	if tgt_dir == None:
		# use current working directory
		tgt_dir = os.getcwd() + "\\"
		file_list = _genFileList_(tgt_dir)
	else:
		if path.exists(tgt_dir):
			# valid file path
			file_list = _genFileList_(tgt_dir)
		else:
			# invalid file path
			print("Invalid directory")
			file_list = []
	return file_list

def CheckFilebyExt(tgt_ext, file_list):
	"""
	Return a list of files that match the extension specified in the
	parameter tgt_ext after searching the file_list parameter.
	It assumes both tgt_ext and file_list contain valid values.
	"""
	match_list = [file for file in file_list
						if file.endswith(tgt_ext)]
	return match_list

def CheckFilebyName(tgt_nm, file_list):
	"""
	Return a list of files that match the name specified in the
	parameter tgt_nm after searching the file_list parameter.
	It assumes both tgt_nm and file_list contain valid values.
	"""
	match_str = path.splitext(tgt_nm)[0] + "*"
	match_list = [file for file in file_list
						if fnmatch.fnmatch(file, match_str)]
	return match_list

def appendNum(file_name, file_list):
	# split name and extension
	f_name, f_extsn = path.splitext(file_name)

	if len(file_list) == 1:
		# no number appended in current existed file
		new_name = f_name + "(2)" + f_extsn
	else:
		# already an appended number
		search_str = re.compile("\(\d+\)")
		app_num = 0
		for file in file_list:
			file_nm, file_ext = path.splitext(file)
			found_match = re.search(search_str, file_nm)
			
			if found_match:
				# found matches
				# remove the "()" in the appended number string
				file_num = int(found_match.group(0)[1:-1])
				if file_num > app_num:
					app_num = file_num

		new_num = app_num + 1	# increment by 1
		new_name = f_name + "(" + str(new_num) + ")" + f_extsn
	return new_name
