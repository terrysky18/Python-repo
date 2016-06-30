"""
The script is to the main logic of GuessNumber.py
"""
playerGuess = -1
guessRemain = -1
secretNum = -1

def input_guess(guess):
	# check whether guess is a number
	if (not guess) or (not guess.isdigit()):
		print "Please enter a proper integer"
		return		# stop the function due to bad input
	# end of if statement

	print ""

	global playerGuess
	playerGuess = int(guess)
	print "Your guess is %d" % playerGuess

	global guessRemain
	guessRemain -= 1

	# still in the game
	if not(playerGuess == secretNum) and guessRemain > 0:
		print "Your remaining guess: %d" % guessRemain

		if playerGuess > secretNum:	# guess is too large
			print "Lower"
		else:				# guess is too small
			print "Higher"

	# out of the game
	elif not(playerGuess == secretNum):
		print "You\'ve run out of guesses.  The number is %d" % secretNum

	# correct guess
	else:
		print "Your remaining guess: %d" % guessRemain
		print "Correct!"
	# end of if-elif-else

# end of input_guess(guess)


guessRemain = 7
secretNum = 18
input_guess("80")
input_guess("12")
input_guess("55")
input_guess("3")
input_guess("8")
input_guess("32")
input_guess("20")


