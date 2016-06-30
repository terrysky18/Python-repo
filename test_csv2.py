"""
A simple script to try writing to a CSV file using csv module
"""

import csv

file_path = 'c:\\users\\jsong\\Documents\\Test cases\\FY15-MR3\\Song DOCSTAT\\testFile.csv'

file_open = open(file_path, 'wb')	# open with wb flag to write
#file_writer = csv.writer(file_open, delimiter=' ', quotechar='|',
#						quoting=csv.QUOTE_NONE)

field_names = ['forename', 'surname']
file_writer = csv.DictWriter(file_open, fieldnames=field_names)

file_writer.writeheader()
file_writer.writerow({'forename':'Terry', 'surname':'Song'})
file_writer.writerow({'forename':'Maya', 'surname':'Kushner'})
file_writer.writerow({'forename':'Maya', 'surname':'Kushner-Song'})

file_open.close()

