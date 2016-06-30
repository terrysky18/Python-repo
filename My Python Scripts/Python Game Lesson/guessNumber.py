"""
This is mini-project #2 in week two, guese the name
Author:  Song, Jiawen (Terry)

Inputs will come from the buttons and the input field of the frame
all outputs for the game will be printed in the console
"""

import random
import simpleguitk as simplegui

# Global variables, all intensionally initialised to -1

playerGuess = -1	# player's guess
guessRemain = -1	# player's remaining number of guesses
secretNum = -1		# the secret number in the game
message = "Guess the secret number"	# message in the canvas
gametype = 1		# the range of the game

# Help functions

def new_game():
	"""
	initialise all global variables whenever a game is started
	"""
	global gametype
	global secretNum
	global guessRemain

	if gametype == 1:	# range [0, 100)
		secretNum = random.randrange(0, 100)

		guessRemain = 7
	
	else:			# range [0, 1000)
		secretNum = random.randrange(0, 1000)

		guessRemain = 10
	
	print "\nYour remaining guess: %d" % guessRemain
# end of new_game() definition

# Define event handlers

def range100():
	"""
	button handler that changes the range to [0, 100) and initiate a new game
	"""
	global gametype
	gametype = 1

	global message
	message = "Guess the secret number"

	new_game()
	
# end of range100() definition

def range1000():
	"""
	button handler that changes the range to [0, 1000) and initiate a new game
	"""
	global gametype
	gametype = 2

	global message
	message = "Guess the secret number"

	new_game()

# end of range1000() definition

def draw(canvas):
	# handler to draw on the canvas
	canvas.draw_text(message, [10, 58], 28, "white")
# end of draw(canvas) definition

def input_guess(guess):
	"""
	the main handler with the game logic, the function receives the
	player's input and determine whether the player guesses correctly
	"""
	# check whether guess is a number
	if (not guess) or (not guess.isdigit()):
		print "Please enter a proper integer"
		return		# stop the function due to bad input
	# end of if statement
	
	global message
	message = "Guess the secret number"

	print ""				# blank line

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

		new_game()

	# correct guess
	else:
		print "Your remaining guess: %d" % guessRemain

		message = "Good job"

		print "Correct!"

		new_game()
	# end of if-elif-else
# end of input_guess(guess)

# Create a frame
frame = simplegui.create_frame("Guess a number", 300, 100)
frame.set_draw_handler(draw)

# Register event handler
frame.add_button("Range [0, 100)", range100, 85)
frame.add_button("Range [0, 1000)", range1000, 85)
frame.add_input("Enter", input_guess, 80)

# Start frame and call a new game
new_game()
frame.start()
