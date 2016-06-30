# untar a tar file with python
# python can open, inspect contents, and extract
#   tar files with the built-in
#   tarfile module.

import tarfile

# tar file to extract
theTarFile = 'example.tar'

# tar file path to extract
extractTarPath = '.'

# open the tar file
tfile = tarfile.open(theTarFile)

if tarfile.is_tarfile(theTarFile):
	# list all contents
	print "tar file contents:"
	print tfile.list(verbose=False)
	# extract all contents
	tfile.extractall(extractTarPath)
else:
	print theTarFile + " is not a tarfile."
