from sys import argv

script, filename = argv

txt = open(filename)

print "\nHere's your file %r: " % filename
print "\n" + txt.read()

content = "\n" + txt.name

print content
print txt.mode
print "Is the file closed? %r" % txt.closed
txt.close()
print "Is the file closed? %r" % txt.closed

#print "\nType the filename again:"
#file_name = raw_input("> ")
#txt_again = open (file_name)
#print txt_again.read()
