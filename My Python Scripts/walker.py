#-------------------------------------------------------------------------------
# Name:        Walker
# Purpose:
#
# Author:      alex.yatsenko
#
# Created:     25/06/2014
# Copyright:   (c) alex.yatsenko 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python



import sys
import os
import hashlib
import errno
from collections import namedtuple
import csv
import time
import win32api
import win32file


print 65*'='
print """
This program will scan all fixed drives for all executables
and record their SHA-1 hashes and file sizes in a CSV file. 
The CSV file will be located in the current working directory
and will be named: <TIMESTAMP>_fileList.csv.

Expected run time is between 5 and 15 minutes depending on 
your system.

NOTE: It will not scan removable, optical, or remote drives.
"""
print 65*'='
print

FileInfo = namedtuple("FileInfo", ["filename", "hash", "filesize"])

def hashfile(filepath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    try:
        with open(filepath, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
    except Exception, e:
        return "Error: " + str(e)
    return hasher.hexdigest()

ext = (
    ".bas", ".bat", ".chm", ".cmd", ".com", ".cpl", 
    ".crt", ".dll", ".exe", ".hlp", ".hta", ".inf", 
    ".ins", ".isp", ".msc", ".msi", ".msp", ".mst", 
    ".pif", ".reg", ".scr", ".sct", ".shb", ".shs", 
    ".sys", ".vb", ".vbe", ".vbs", ".wsc", ".wsf", 
    ".wsh"
)
#
# Identify all of the drives
#
paths=list()
allDrives = win32api.GetLogicalDriveStrings().split("\x00")[:-1]
for drive in allDrives:
    try:
        volumeInfo = win32api.GetVolumeInformation(drive)
        if volumeInfo[4] == "NTFS" or "FAT" in volumeInfo[4]:
            if win32file.GetDriveType(drive) == win32file.DRIVE_FIXED:
                paths.append(drive)
    except Exception as e:
        print e
        continue
#
# Walk the drives and look for file names that end with something 
# in the ext list above
#
print "Walking: " + str(paths)

fileList = list()
counter = 0
start = time.time()
last_check = None
for path in paths:
    print "Walking", path
    
    if not path: continue
    if not os.path.exists(path): continue

    for root, dirs, files in os.walk(path):
        for fileName in files:
            cur_time = int(time.time())
            if cur_time % 5 == 0 and cur_time != last_check: 
                print "[{0}] Files Processed: {1}".format(path, counter)
                last_check = cur_time
            fileNameNoExt, fileExtension = os.path.splitext(fileName)

            if not fileExtension.lower() in ext: continue

            fullFile = os.path.join(root,fileName)
            size = os.path.getsize(fullFile)
            hash = hashfile(fullFile)
            if "Error" not in hash:
                fileList.append(FileInfo(filename=fullFile, hash=hash, filesize=size))
                counter = counter + 1
            else:
                print "Error processing:", fullFile, hash
                print "The above is most probably normal and expected due to permissions."


print "Total number of files processed: " + str(counter),"in", int(time.time() - start), "seconds."

#print fileList
epoch_time = int(time.time())
output= str(epoch_time) + "_" + "fileList.csv"

with open(output, 'wb') as result:
    writer = csv.writer(result, dialect='excel')
    writer.writerow(['file_name', 'sha1', 'file_size'])
    writer.writerows(fileList)
