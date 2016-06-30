# Following the example in Sqlite turtorial
# this file creates the database file in a specified directory

import sqlite3

# create a connection object to represent the database
conn = sqlite3.connect("C:\\Users\\terry.song\\Documents\\my python scripts\\database\\example.db")

# create a cursor object to perform SQL commands
cur = conn.cursor()

# create table
cur.execute('''CREATE TABLE stocks
		(date text, trans text, symbol text, qty real, price real)''')

# insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100, 35.14)")
cur.execute("INSERT INTO stocks VALUES ('2006-01-08', 'BUY', 'LMT', 108, 48.32)")

# save (commit) the changes
conn.commit()

# close the connection if finished
# all changes need to be committed or they will be lost

conn.close()
