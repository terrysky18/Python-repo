import re
import xml.etree.ElementTree as ElemTree
import os

class CBAXMLParser(object):
	"""
	A class to read a production CBA XML file and extract data to allow further
	processing the analysis
	"""

	def __init__(self):
		# class constructor
		self._file_date = ''
		self._file_account = []
		self._file_data = []

	def __CheckFile__(self, subject_file):
		# check whether the subject file and return absolute file path if exists
		work_direct = os.getcwd()
		file_direct = os.path.dirname(os.path.abspath(__file__))
		path1 = work_direct + '\\' + subject_file
		path2 = file_direct + '\\' + subject_file

		if path1 == path2:
			return os.path.exists(path1)

		else:
			if os.path.exists(path1) or os.path.exists(path2):
				return True
			else:
				return False

	def ReadFile(self, subject_file):
		# Parse the subject xml file and save the data
		file_path = self.__CheckFile__(subject_file)

		if file_path:
			file_data = ElemTree.parse(subject_file)
			data_root = file_data.getroot()

			# parse file date
			self._file_date = data_root[0].text
			# parse the account information
			self.ReadAccountInfo(data_root[1])

			# parse the transaction information
			for tran_idx in range(2, len(data_root)):
				self.ReadTransactions(data_root[tran_idx])


	def ReadAccountInfo(self, data_ary):
		# Parse the account information from the parsed subject xml file
		# data_ary is a data array containing the account information of a CBA
		for idx in range(len(data_ary)):
			data_key = removeExcess(data_ary[idx].tag)
			self._file_account.append({data_key: data_ary[idx].text})

	def ReadTransactions(self, data_ary):
		# Parse 1 transaction information from the subject xml file
		# data_ary is a data array containing the transaction information of a CBA
		trans_entry = []
		for idx in range(len(data_ary)):
			data_key = removeExcess(data_ary[idx].tag)
			trans_entry.append({data_key: data_ary[idx].text})

		self._file_data.append(trans_entry)


	def GetFileDate(self):
		# return the date of the file as a string
		return self._file_date

	def GetNumTrans(self):
		# return the number of transactions in the xml file
		return len(self._file_data)

	def GetNumAccountEntry(self):
		# return the number of entries in account information
		return len(self._file_account)

	def GetNumTransEntry(self):
		# return the number of entries in transaction information
		return len(self._file_data[0])


	def PrintAccountInfo(self):
		# return a string with account tags and corresponding values
		account_str = ""
		for idx in range(len(self._file_account)):
			tag_ary = list(self._file_account[idx].keys())
			val_ary = list(self._file_account[idx].values())
			# arrays only contain 1 element
			account_str += printEntry(tag_ary[0], val_ary[0])

		return account_str

	def GetAccountTag(self):
		# return a list of strings containing account tags
		# used for exporting to excel
		tag_ary = []
		for idx in range(len(self._file_account)):
			temp_ary = list(self._file_account[idx].keys())
			tag_ary.append(temp_ary[0])

		return tag_ary

	def GetAccountVal(self):
		# return a list of strings containing account values
		# used for exporting to excel
		val_ary = []
		for idx in range(len(self._file_account)):
			temp_ary = list(self._file_account[idx].values())
			if temp_ary[0]:
				val_ary.append(temp_ary[0])
			else:
				# handles None value
				val_ary.append(str(temp_ary[0]))

		return val_ary

	def PrintTransaction(self, trans_num=None):
		# return a string with transaction tag and corresponding values
		# trans_num is the index of the transaction list
		# if trans_num is not passed, the entire transaction list is returned
		trans_str = ""

		if trans_num==None:
			# transaction index not passed
			for idx in range(len(self._file_data)):
				for jdx in range(len(self._file_data[idx])):
					tag_ary = list(self._file_data[idx][jdx].keys())
					val_ary = list(self._file_data[idx][jdx].values())
					trans_str += printEntry(tag_ary[0], val_ary[0])
				trans_str += "\n"
		else:
			# receives transaction index
			if trans_num < len(self._file_data):
				# index within data list
				for idx in range(len(self._file_data[trans_num])):
					tag_ary = list(self._file_data[trans_num][idx].keys())
					val_ary = list(self._file_data[trans_num][idx].values())
					trans_str += printEntry(tag_ary[0], val_ary[0])
			else:
				print("Error:  entry index out of list range")

		return trans_str

	def GetTransTag(self):
		# return a list of strings containing transaction tags
		# the function does not take an index parameter because the
		# tags are identical for all transactions
		# used for exporting to excel
		tag_ary = []
		for idx in range(len(self._file_data[0])):
			temp_ary = list(self._file_data[0][idx].keys())
			tag_ary.append(temp_ary[0])
		return tag_ary

	def GetTransVal(self, trans_num=None):
		# return a list of strings containing transaction values
		# used for exporting to excel
		# trans_num is the index of the transaction list
		# if trans_num is not passed, the entire transaction list is returned as a matrix
		# if trans_num is passed, the corresponding transaction is returned as a list
		trans_val = []

		if trans_num==None:
			# transaction index not passed
			for idx in range(len(self._file_data)):
				entry_val = []
				for jdx in range(len(self._file_data[idx])):
					temp_ary = list(self._file_data[idx][jdx].values())
					if temp_ary[0]:
						# handle None value
						entry_val.append(temp_ary[0])
					else:
						entry_val.append(str(temp_ary[0]))
				trans_val.append(entry_val)
		else:
			# transaction index passed
			if trans_num < len(self._file_data):
				# index within data list
				for idx in range(len(self._file_data[trans_num])):
					temp_ary = list(self._file_data[trans_num][idx].values())
					if temp_ary[0]:
						# handle None value
						trans_val.append(temp_ary[0])
					else:
						trans_val.append(str(temp_ary[0]))
			else:
				print("Error:  entry index out of list range")

		return trans_val


# Helper functions
def removeExcess(data_str):
	# The function checks to remove {http://www.ngc.com/DTS/CBAGEXTransaction}
	to_remove = '\{([^}]+)\}'	#URL in xml tag
	output_str = re.sub(to_remove, '', data_str)
	return output_str

def printEntry(tag_str, val_str):
	# helper function to construct a print string
	# return entry with new line
	output_str = tag_str
	output_str += ":  "
	if val_str:
		# handle None value
		output_str += val_str
	output_str += "\n"
	return output_str

