"""
A simple script to demonstrate the use of dictionary type
"""

import simpleguitk as simplegui
import random

CIPHER = {}
LETTERS = " abcdefghijklmnopqrstuvwxyz@."

message = ""

# helper function
def init():
	letter_list = list(LETTERS)
	random.shuffle(letter_list)	# scrambles the letter list

	for ch in LETTERS:		# construct the dictionary
		# pop() returns and removes the last element of the list
		CIPHER[ch] = letter_list.pop()
	"""
	CIPHER now cotains original letter list as key, scrambed list as value
	"""

# button handler

def encode():		# encode handler
	encodedM = ""
	for ch in message:	# message is the original value
		encodedM += CIPHER[ch]
	print message, "encodes to ", encodedM
# end of encode()

def decode():		# decode handler
	decodedM = ""

	for ch in message:	# message is the encoded value
		for key, value in CIPHER.items():	# iterate key & values
			if ch == value:
				decodedM += key
				# key in CIPHER is the original list
	
	print message, "decodes to ", decodedM

# text field handler

def newmsg(msg):
	global message
	message = msg
	label.set_text(msg)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("CIPHER", 20, 200, 200)
frame.add_input("Message: ", newmsg, 200)
label = frame.add_label("")
frame.add_button("Encode", encode)
frame.add_button("Decode", decode)

init()		# initialise
frame.start()

