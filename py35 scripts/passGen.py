"""
A script to generate a strong password to satisfy the for-ever present
requirement to use a new password
"""

from FileWriter import FileWriter
import string		# needed to create alphabet list
import random
import argparse

# debugger boolean
debug = True

def ArgParser():
	# contruct an argument parser
	help_description = """A convenient script to generate and store
	passwords.  The password satisfies typical requirements for upper and
	lower with digits and special characters.  Different options can be
	used to select the use of special characters and logging the
	passwords."""

	parser = argparse.ArgumentParser(description=help_description)
	
	num_char_arg_help = """An optional argument to specify number of
	characters in the password.  Default value is 16."""

	parser.add_argument('num_char', nargs='?', default=16, help=num_char_arg_help)

	spec_char_arg_help = """An optional argument to select use of special
	characters in the password.  Default value is y."""

	parser.add_argument('special_char', nargs='?', default='y', help=spec_char_arg_help)

	pass_log_arg_help = """An optional argument to select logging the
	generated password.  Default value is y."""

	parser.add_argument('gen_pass_log', nargs='?', default='y', help=pass_log_arg_help)

	args = parser.parse_args()
	if debug:
		print(type(args))
		print(args)

	return args

def GenPassW(num_char, spec_char):
	"""
	Generate a password in the length specified by parameter num_char.
	The default length is 8
	"""
	alpha_upper = list(string.ascii_uppercase)
	alpha_lower = list(string.ascii_lowercase)
	numeric_str = list(string.digits)

	special_str = r"!$%&()*+-:<=>?@[]^_{}~"
	special_char = list(special_str)

	# randomise the character lists
	random.shuffle(alpha_upper)
	random.shuffle(alpha_lower)
	random.shuffle(numeric_str)
	random.shuffle(special_char)

	if debug:
		print(alpha_upper)
		print(alpha_lower)
		print(numeric_str)
		print(special_char)

	# initialise indices
	i_upper = 0
	i_lower = 0
	i_numeric = 0
	i_special = 0

	result_list = []
	while len(result_list) < num_char:
		i_upper = AddChar(result_list, alpha_upper, i_upper)
		i_lower = AddChar(result_list, alpha_lower, i_lower)
		i_numeric = AddChar(result_list, numeric_str, i_numeric)
		if spec_char == 'y':
			i_special = AddChar(result_list, special_char, i_special)

		if debug:
			print(len(result_list))

	# randomise the result list once more
	random.shuffle(result_list)
	result_str = "".join(result_list)

	if debug:
		print(result_str)

	return result_str

def AddChar(tgt_list, src_list, src_idx):
	"""
	Add the character from the source list to the target list.  The source
	list character is indicated by the source index.  The function
	increments and returns the index value
	"""
	tgt_list.append(src_list[src_idx])
	src_idx+=1
	return src_idx


if __name__ == '__main__':
	my_args = ArgParser()
	char_num = int(my_args.num_char)
	use_spec = my_args.special_char
	use_log = my_args.gen_pass_log

	Password_file = r"C:\Users\Terry Song\Documents\Repository\Python-repo\py-Logs\test_pass.txt"
	my_logger = FileWriter(Password_file)
	my_stuff = GenPassW(char_num, use_spec)

	if debug:
		print(type(my_stuff))
		print(my_stuff)

	if use_log == 'y':
		my_logger.WriteItDown("New Password: " + my_stuff)
