"""
A simple class that writes contents to a file in a specific directory.
If the file does not exist, it creates the file.  If the file already exists,
it appends the input text to the content of the file.


def __init__(self, file_loc=None):
	class constructor
	parameter:
		file_loc specifies the directory of the log file.  If the parameter isn't passed
		to the constructor, the log file will be saved to the hard coded default directory


"""

import os.path as checkPath
import datetime

class FileWriter(object):

	# class constructor
	def __init__(self, file_loc=None):
		"""
		FileWriter class constructor
		"""
		# the file location is not specified
		if not file_loc:
			self._file_path = "C:\\Users\\jsong\\Documents\\Python scripts\\py-Logs\\Log_file01.txt"
		# file location is specified
		else:
			self._file_path = file_loc

		self.Start()

	def Start(self):
		"""
		Initiate the file if the file does not exist
		"""
		file_exist = checkPath.exists(self._file_path)
		# file does not exist, create it
		if not file_exist:
			write_file = open(self._file_path, 'w')
			time_stamp = self.GetTimeStamp()
			temp = "Starting new file log, " + time_stamp
			write_file.write(temp)
			write_file.close()
	
	def WriteItDown(self, to_write):
		"""
		Receives the content to write in the file in the parameter.
		"""
		# make sure to_write is not an empty string
		if to_write:
			write_file = open(self._file_path, 'a')
			time_stamp = '\n'*2 + self.GetTimeStamp()
			write_file.write(time_stamp)
			content = '\n' + to_write
			write_file.write(content)
			write_file.close()

	def GetTimeStamp(self):
		"""
		A function that returns the current time stamp string.
		Not sure whether it's entirely necessary.  The datetime function is
		only one line, but keep it for now.
		"""
		# obtain system stamp
		time_now = datetime.datetime.now().strftime("%d %B %Y %H:%M")
		return time_now

