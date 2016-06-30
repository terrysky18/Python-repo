import re

# \s = space
# \S = non-space
# \d = digits
# \D = non-digits

# \s - space character in a string
# * - any number of the instance in front of *
# split - takes 2 parameters, splits the second parameter according to pattern
#	specified by first parameter, produces a list

#print re.split(r'\s*', 'here are some words')

# () - in the first parameter means include the specified pattern in the result

#print re.split(r'(\s*)', 'here are some words')

# without \ the string is split at the character s

#print re.split(r'(s*)', 'here are some words')

# [a-z] = find a range of characters
# re.I = Ignore case
# re.M = Multiline
# [a-f][a-f] = letter right beside each other
print re.split(r'[a-fA-F]', 'I am just practising python regular expression, IT IS COMPLETELY NOT EASY AT ALL'), re.I|re.M
