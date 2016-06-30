"""
An random account number generator
It generates an account number to be used for testing in different environment
"""

import random
import argparse
from Tkinter import Tk
import string		# needed to create alphabet list

# debugger boolean
debug = False

def genAccNum(acc_length):
	"""
	Takes an integer parameter and use it to determine the length of the
	returned string.
	Returns a randomly generated alphanumeric string
	"""
	if acc_length > 0:
		if acc_length > 15:
			num_array = range(acc_length*2)
		else:
			num_array = range(10)
		alpha_array = list(string.ascii_uppercase)

		if debug:
			print(num_array)
			print(alpha_array)

		# randomise the arrays
		random.shuffle(num_array)
		random.shuffle(alpha_array)

		if debug:
			print(num_array)
			print(alpha_array)

		acc_num_str = ""
		array_idx = 0
		while len(acc_num_str) < acc_length:
			if debug:
				print("array index: %d" % array_idx)
				print(acc_num_str)

			acc_num_str += alpha_array[array_idx]
			acc_num_str += alpha_array[array_idx + 1]
			acc_num_str += str(num_array[array_idx])
			acc_num_str += str(num_array[array_idx + 1])
			array_idx += 2

		if len(acc_num_str) > acc_length:
			#result is too long; truncate the extra bit
			acc_num_str = acc_num_str[:acc_length]

		return acc_num_str
	else:
		print("String length must be positive")


if __name__ == '__main__':
	"""
	construct an argument parser
	Takes an argument parameter from user inputer, parses the arugment,
	returns a parsed argument object
	"""
	help_description = """A convenient script to generate account numbers
	used for testing in different users accounts.  The account numbers
	are indeed fictitious and cannot be used in real life environment.
	  The script receives an argument for the length of account numbers.
	  The default account number length is eight alphanumeric characters."""

	parser = argparse.ArgumentParser(description = help_description)

	help_argument = """An optional argument determines the length of
	the generated account number."""

	parser.add_argument('optional_arg', nargs='?', default="8",\
			help=help_argument)

	args = parser.parse_args()
	if debug:
		print(args.optional_arg)
		print(type(args.optional_arg))

	in_str = args.optional_arg
	if in_str.isdigit():
		str_length = int(in_str)
		acc_str = genAccNum(str_length)

		# copy to clipboard
		print(acc_str)
		copier = Tk()
		copier.withdraw()
		copier.clipboard_clear()
		copier.clipboard_append(acc_str)
		copier.destroy()
	else:
		print("Argument must an integer")

