import re
import DirectoryFileMod as dirFile

def IDfile():
	"""
	Identify the XML file in current directory of the script and return
	name of the file
	"""
	# target file's name begins with ETIC and ends with xml extension
	tgt_str = "^(ETIC)"
	tgt_ext = ".xml"
	
	cur_dir_file = dirFile.GetFileList()
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

correct_file = IDfile()
print(correct_file)
