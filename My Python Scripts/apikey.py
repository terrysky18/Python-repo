from sys import argv
from Tkinter import Tk		# needed to copy to clipboard

script, key_select = argv

copier = Tk()			# create a copier object from Tk class

copier.withdraw()
copier.clipboard_clear()	# clear the clipboard

virustotal = '977f41f0fd1ff9a674117af52aba748528f760507fa5a8041b7522f30c0d2e3d'
metascan = '213df45988896ed79661def5f3fea87a'

if ('1' in key_select):
	print 'virus total'
	copier.clipboard_append(virustotal)	# copy the virus total api key

elif ('2' in key_select):
	print 'metascan'
	copier.clipboard_append(metascan)	# copy the metascan api key

else:
	print 'Parameter not recognised'

copier.destroy()

