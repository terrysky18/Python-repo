"""
Basic MySQLdb use with Python

Showing basic syntax of MySQLdb
It does not connect to an actual database
"""

import MySQLdb as mysql

# connect to the database
db = mysql.connect(host = "localhost", # my host, usually localhost
		user = "terry",		# my username
		passwd = "power!",	# my password
		db = "tutorial1")	# name of the database

# create a cursor object
cursor = db.cursor()

# execute queries
cursor.execute("SELECT * FROM database_table")

# do what need to be done with the data
for row in cursor.fetchall():
	print(row[0])

