import sys, time

i = 0

for i in range(10):
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(0.5)
