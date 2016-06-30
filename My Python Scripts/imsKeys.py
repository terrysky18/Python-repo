# from sys import argv
from Tkinter import Tk	# needed to copy key clipboard

# script, key_select = argv

copier = Tk()	# create copier object from Tk class

copier.withdraw()
copier.clipboard_clear()	#clear the clipboard

# IMS licence keys
licences = {1:["CMS only", "79427457458150042113"],
			2:["TDS only", "16994300676501400670"],
			3:["SEN only", "28411271575728174727"],
			4:["CMS & TDS", "96771050191964281052"],
			5:["CMS & SEN", "03503762135007010555"],
			6:["TDS & SEN", "86068143661589810660"],
			7:["all 3", "53019390921719757698"]}

print 'available IMS licence keys'
for key in licences:
	print key, ': ', licences[key][0]

key_select = raw_input('which key to use? ')

if ('1' in key_select):
	print "CMS only"
	copier.clipboard_append(licences[1][1])
	
elif ('2' in key_select):
	print "TDS only"
	copier.clipboard_append(licences[2][1])
	
elif ('3' in key_select):
	print "Invisibility only"
	copier.clipboard_append(licences[3][1])

elif ('4' in key_select):
	print "CMS and TDS"
	copier.clipboard_append(licences[4][1])

elif ('5' in key_select):
	print "CMS and Invisibility"
	copier.clipboard_append(licences[5][1])

elif ('6' in key_select):
	print "TDS and Invisibility"
	copier.clipboard_append(licences[6][1])

elif ('7' in key_select):
	print "CMS, TDS, Invisibility"
	copier.clipboard_append(licences[7][1])
	
else:
	print 'Parameter not recognised'
	pass

copier.destroy()
