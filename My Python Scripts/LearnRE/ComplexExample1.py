import re

# \s = space
# \S = non-space
# \d = digits same as [0-9]
# \D = non-digits
# \w = alphanumeric
# \. = regular period .
# . = any character but newline (\n)

# quantities:
# * = 0 or more
# + = 1 or more
# ? = 0 or 1 of
# {5} = exact number of
# {1, 60} = range on number, minimum of 1, maximum of 60

# \w+ because we may not know number of letters in street name

print re.findall(r'\d{1,5}\s\w+\s\w+\.', 'lwkeoiuancz338 main st.ncox;qmx'), re.I|re.M
