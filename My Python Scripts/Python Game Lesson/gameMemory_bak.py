"""
week 5 mini project - Memory
Author:  Song, Jiawen (Terry)
"""
import simpleguitk as simplegui
import random

# global constants
CARD_WIDTH = 45
CARD_HEIGHT = 110
CARD_COLOUR = 'silver'
GAP_WIDTH = 6
FIRST_CARD_LOC = [7, 13]	# coordinates of first card's upper left corner

# global variables
mouseklik_pos = ()		# mouse click position
card_turned = 0			# number of times play turns cards
card_deck = []			# deck of cards used in the game
cardLoc = []			# coordinates of each card's upper left corner
exposed_card = []		# track which card is revealed
state = 0			# game state logic variable

# helper function to initialise global variables
def new_game():
	global mouseklik_pos, card_turned, state
	global card_deck, cardLoc, exposed_card

	mouseklik_pos = (0, 0)
	card_turned = 0
	card_deck = range(8)	# initial deck from 0 to 7
	card_deck += card_deck	# add a pair to the initial deck
	random.shuffle(card_deck)
	
	cardLoc = [FIRST_CARD_LOC]	# coordinates of cards upper left corner
	cnt = 1				# counter used in loop
	stop = len(card_deck)

	# construct the list of card coordinates
	while cnt < stop:
		temp_loc = [cardLoc[0][0] + cnt*CARD_WIDTH + cnt*GAP_WIDTH, cardLoc[0][1]]
		cardLoc.append(temp_loc)
		cnt += 1	# increment the counter
		# end of while loop
	
	exposed_card = [False] * len(card_deck)		# all cards covered
	state = 0
# end of new_game()

# define event handlers
def mouseclick(pos):
	# game state logic here
	global mouseklik_pos, cardLoc, exposed_card, state, card_turned
	global card_deck

	mouseklik_pos = pos

	# check if any card is clicked
	cnt = 0
	for lst in cardLoc:
		# mouse click horizontal boolean check
		hori_check = (mouseklik_pos[0] > lst[0]) and (mouseklik_pos[0] < (lst[0] + CARD_WIDTH))
		# mouse click vertical boolean check
		verti_check = (mouseklik_pos[1] > lst[1]) and (mouseklik_pos[1] < (lst[1] + CARD_HEIGHT))

		if hori_check and verti_check:	# a card is clicked
			match = False		# boolean check between cards

			if not exposed_card[cnt]:
				if state == 0:	# no card has been revealed
					state = 1
					exposed_card[cnt] = True
					card_turned += 1

				elif state == 1:	# 1 card's been revealed
					state = 2
					exposed_card[cnt] = True
					card_turned += 1

				else:
					state = 1
					exposed_card = [False] * len(exposed_card)
					exposed_card[cnt] = True
					card_turned += 1
					# end of if-elif-else
			else:	# card already revealed
				pass
		else:	# clicked outside a card
			pass
			# end of if-else
		cnt += 1
		# end of for loop
	temp_text = "Turn = " + str(card_turned)
	label.set_text(temp_text)
	
# end of mouseclick()

def draw(canvas):
	global card_deck, cardLoc
	global mouseklik_pos, exposed_card

	# draw cards
	cnt = 0			# index used in loop
	for lst in cardLoc:
		if not exposed_card[cnt]:	# card not exposed
			cardPoints = [[lst[0], lst[1]], [lst[0]+CARD_WIDTH, lst[1]], [lst[0]+CARD_WIDTH, lst[1]+CARD_HEIGHT], [lst[0], lst[1]+CARD_HEIGHT]]
			canvas.draw_polygon(cardPoints, 2, CARD_COLOUR, CARD_COLOUR)
		else:		# card exposed
			temp_text = str(card_deck[cnt])
			canvas.draw_text(temp_text, [lst[0], lst[1]+CARD_HEIGHT], 62, 'white')
			# end of if-else

		cnt += 1	# increment the index
		# end of for loop
# end of draw()

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 820, 100)
frame.add_button("Reset", new_game, 80)
label = frame.add_label("Turn = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

