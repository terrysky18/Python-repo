import sqlite3
from sqlite3 import Error

def connectToDBFile(db_file):
	"""
	Make a connection to the database specified in the parameter
	param:  db_file - path to database connection
	return:  conn object
	"""
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print("Database connection error")

def selectData(conn):
	"""
	Select all rows in a database from a specified table
	param:  conn - database connection object
	param:  table_name - table to select rows
	return:  dictionary of companies with all departments and employees
	"""
	my_data = {}
	my_cursor = conn.cursor()
	my_cursor.execute("SELECT * FROM {tn}".format(tn="Company"))
	all_companies = my_cursor.fectchall()

	# Construct list of department and employee for each company
	for company in all_companies:
		my_data[company] = []
		# Query the department table
		my_cursor.execute("SELECT * FROM {tn} WHERE Company={cn}".format(tn="Department", cn=company))
		all_departments = my_cursor.fetchall()
		department_dict = {}
		department_dict["Department"] = []
		for department in all_departments:
			department_dict["Department"].append(department)
		# Add the list of department to the corresponding company
		my_data[company].append(department_dict)

		# Query the employee table
		my_cursor.execute("SELECT * FROM {tn} WHERE Company={cn}".format(tn="Employee", cn=company))
		all_employees = my_cursor.fetchall()
		employee_dict = {}
		employee_dict["Employee"] = []
		for employee in all_employees:
			employee_dict["Employee"].append(employee)
		# Add the list of employees to the corresponding company
		my_data[company].append(employee_dict)

	return my_data

if __name__ == "__main__":
	db_file = r"C:\Users\user\Documents\test.db"
	connect = connectToDBFile(db_file)
	company_data = selectData(connect)
