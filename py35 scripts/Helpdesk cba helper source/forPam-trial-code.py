"""
A programme to assistant Defence Travel System help desk analyst extract useful data
from CBA xml files from production environments
"""

import xml.etree.ElementTree as ElemTree
import argparse
import os

# debugger boolean
# set to True enable debug printout
debug = False
file_path = os.path.dirname(os.path.abspath(__file__))
file_name = 'ETIC-7687_201608347091C.xml'

subject_file = file_path + '\\' + file_name

if debug:
	print("POWER!")
	print(file_path)
	print(subject_file)

if os.path.exists(subject_file):
	print("found it")
else:
	print("look again")

# file_data - ElementTree type
file_data = ElemTree.parse(subject_file)

# data_root - Element type
data_root = file_data.getroot()
print(data_root.tag)
#print(data_root.attrib)

data_list = list(data_root)
print(len(data_list))
print(data_list[1][0].tag)
print(data_list[1][0].text)

