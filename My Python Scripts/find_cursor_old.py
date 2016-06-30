from Mouse import Mouse
import time

cursor = Mouse()

pos = cursor.get_position()
print pos

start_time = time.time()			# start time stamp
elapsed_time = time.time() - start_time		# elapsed time

max_elapsed = 3600		# maximum elapsed time, 60 minutes

while (elapsed_time < max_elapsed):
	if (not(pos == cursor.get_position())):
		pos = cursor.get_position()	# if the mouse moves, update it
		print pos

	# end if statement
# end of while loop
