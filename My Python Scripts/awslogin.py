from Tkinter import Tk	# needed to copy key clipboard


copier = Tk()	# create copier object from Tk class

copier.withdraw()
copier.clipboard_clear()	#clear the clipboard

passwd = r'*NV*DWknqqyY9f'

copier.clipboard_append(passwd)		#copy the string to clipboard

copier.destroy()

print 'username: alan.keister@invincea.com'
