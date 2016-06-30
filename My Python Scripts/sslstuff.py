from sys import argv
from Tkinter import Tk

script, key_select = argv

copier = Tk()

copier.withdraw()
copier.clipboard_clear()

ssl_cert = r'/etc/pki/tls/certs/ims.crt'
ssl_key = r'/etc/pki/tls/private/ims.key'
ssl_version = r'SSLv23'

if ('1' in key_select):
	print 'ssl_cert'
	copier.clipboard_append(ssl_cert)

elif ('2' in key_select):
	print 'ssl_key'
	copier.clipboard_append(ssl_key)

elif ('3' in key_select):
	print 'ssl_version'
	copier.clipboard_append(ssl_version)

else:
	print 'Parameter not recognised'

copier.destroy()

