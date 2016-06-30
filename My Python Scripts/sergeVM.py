from Tkinter import Tk	# needed to copy key clipboard


copier = Tk()	# create copier object from Tk class

copier.withdraw()
copier.clipboard_clear()	#clear the clipboard

passwd = r'OMGPasswordsWTF!'

copier.clipboard_append(passwd)		#copy the string to clipboard

copier.destroy()

print 'IP: 10.9.13.31'
print 'username: admin'
