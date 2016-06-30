"""
A script to generate a series of random numbers to be used for accounting data
fields.
The script does not work with Python 3.5 due to tkinter issue
"""

import string
import random
import argparse
from Tkinter import Tk

# debugger boolean
debug = False

def argParser():
	# construct an argument parser
	help_description = """A convenient script to generate a set of random
	numbers to be used as data in account system testing.  The positional
	argument specifies number of digits to generate."""

	parser = argparse.ArgumentParser(description=help_description)

	arg_help = """The argument specifies the number of digits to generate.
	The argument does not have a default value and is required."""

	parser.add_argument('num_digit', metavar='N', type=int, nargs='+',
			help=arg_help)
	args = parser.parse_args()

	if debug:
		print(args.num_digit)

	return args.num_digit[0]

def genDigits(num_gen):
	"""
	Generates a set of random numbers.  The parameter num_gen specifies
	the number of digits to generate.
	"""
	num_str = ""
	for i in range(num_gen):
		num_str += str(random.randrange(0, 10))

	if debug:
		print(num_str)

	return num_str

def copyToClipboard(copy_str):
	"""
	send the string to the window clipboard
	"""
	copier = Tk()
	# keep the window from showing
	copier.withdraw()
	copier.clipboard_clear()
	# text saved to clipboard
	copier.clipboard_append(copy_str)
	copier.destroy()

if __name__ == '__main__':
	gen_num = argParser()

	if debug:
		print(type(gen_num))

	gen_str = genDigits(gen_num)
	copyToClipboard(gen_str)
	print(gen_str)

