import DirectoryFileMod as dirFile

my_py_files = dirFile.GetFileList()
print(my_py_files)

my_matches = dirFile.CheckFilebyExt("xlsx", my_py_files)
print(my_matches)

file_matches = dirFile.CheckFilebyName("cba", my_matches)
print(file_matches)

#print(dirFile.GetFileList("d:\\Users\\"))
