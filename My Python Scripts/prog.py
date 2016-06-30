# A practise script for learning Python Argparse module

import argparse

# define the argument parser
parser = argparse.ArgumentParser(description='calculate X to the power of Y')
# define the positional argument
parser.add_argument('x', type=int, help='the base')
parser.add_argument('y', type=int, help='the exponent')

# define conflictly optional argument
group = parser.add_mutually_exclusive_group()
# define the optional arguments
group.add_argument('-v', '--verbose', action='store_true', default=None)
group.add_argument('-q', '--quiet', action='store_true', default=None)

# the operation
args = parser.parse_args()	#parse the arguments
answer = args.x**args.y	#action performed on the positional argument

if args.quiet:
	print answer
elif args.verbose:
	print '{} to the power {} equals {}'.format(args.x, args.y, answer)
else:
	print '{}^{} == {}'.format(args.x, args.y, answer)
