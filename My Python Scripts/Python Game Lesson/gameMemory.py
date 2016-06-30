"""
week 5 mini project - Memory
Author:  Song, Jiawen (Terry)
"""
import simpleguitk as simplegui
import random

# global constants
CARD_WIDTH = 71
CARD_HEIGHT = 96
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)
CARD_CENTRE = (CARD_WIDTH / 2, CARD_HEIGHT / 2)
card_back_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")
GAP_WIDTH = 3
FIRST_CARD_LOC = [4, 22]	# coordinates of first card's upper left corner
NUM_SIZE = 60

# global variables
mouseklik_pos = ()		# mouse click position
num_klik = 0			# number of click by player
card_turned = 0			# number of times play turns cards
card_deck = []			# deck of cards used in the game
cardLoc = []			# coordinates of each card's upper left corner
exposed_card = {}		# track which card is revealed
state = 0				# game state logic variable

# helper function to initialise global variables
def new_game():
	global mouseklik_pos, card_turned, state
	global card_deck, cardLoc, exposed_card, num_klik

	mouseklik_pos = (0, 0)
	num_klik = 0
	card_turned = 0
	card_deck = range(8)	# initial deck from 0 to 7
	card_deck += card_deck	# add a pair to the initial deck
	random.shuffle(card_deck)
	exposed_card[0] = [False, 'unmatched']
	cardLoc = [FIRST_CARD_LOC]	# coordinates of cards upper left corner
	state = 0
	
	cnt = 1					# counter used in loop
	stop = len(card_deck)
	# construct the list of card coordinates, initialise exposed_card
	while cnt < stop:
		temp_loc = [cardLoc[0][0] + cnt*CARD_WIDTH + cnt*GAP_WIDTH, cardLoc[0][1]]
		cardLoc.append(temp_loc)
		
		exposed_card[cnt] = [False, 'unmatched']
		cnt += 1	# increment the counter
	
	label.set_text("Turn = " + str(card_turned))	# update label

# helper function to determine if cards match
def match_maker2():
# check if the two revealed card values match
# if matched, exposed_card is updated, if mismatched nothing happens
# regardless matching, both cards stay revealed
	global card_deck, exposed_card, state
	
	match = []
	for idx in exposed_card:
		if exposed_card[idx][0] and exposed_card[idx][1] == 'unmatched':
			match.append(idx)
	
	# match only has 2 deck indices
	if card_deck[match[0]] == card_deck[match[1]]:
		exposed_card[match[0]][1] = 'matched'
		exposed_card[match[1]][1] = 'matched'
		state = 0	# reset the state when matched

def match_maker3(card_idx):
# check if the three revealed card values match
# if matched, exposed_card is updated, if mismatched the last card stays revealed
	global card_deck, exposed_card, state
	
	match = []
	for idx in exposed_card:
		if exposed_card[idx][0] and exposed_card[idx][1] == 'unmatched':
			match.append(idx)
	
	# match has 3 deck indices
	if card_deck[match[0]] == card_deck[match[1]]:
		exposed_card[match[0]][1] = 'matched'
		exposed_card[match[1]][1] = 'matched'
		exposed_card[match[2]][0] = False	# cover the unmatched card
		state = 0	# reset the state when matched
	elif card_deck[match[0]] == card_deck[match[2]]:
		exposed_card[match[0]][1] = 'matched'
		exposed_card[match[2]][1] = 'matched'
		exposed_card[match[1]][0] = False	# cover the unmatched card
		state = 0	# reset the state when matched
	elif card_deck[match[1]] == card_deck[match[2]]:
		exposed_card[match[1]][1] = 'matched'
		exposed_card[match[2]][1] = 'matched'
		exposed_card[match[0]][0] = False	# cover the unmatched card
		state = 0	# reset the state when matched
	else:		# no match at all
		for idx in exposed_card:
			if exposed_card[idx][1] == 'unmatched' and (not idx == card_idx):
				exposed_card[idx][0] = False

		state = 1

# define event handlers
def mouseclick(pos):
	# game state logic here
	global mouseklik_pos, cardLoc, exposed_card, state, card_turned
	global card_deck, num_klik

	mouseklik_pos = pos

	# check if any card is clicked
	cnt = 0
	for lst in cardLoc:
		# mouse click horizontal boolean check
		hori_check = (mouseklik_pos[0] > lst[0]) and (mouseklik_pos[0] < (lst[0] + CARD_WIDTH))
		# mouse click vertical boolean check
		verti_check = (mouseklik_pos[1] > lst[1]) and (mouseklik_pos[1] < (lst[1] + CARD_HEIGHT))

		if hori_check and verti_check:	# a card is clicked
			if not exposed_card[cnt][0]:	# clicks a covered card
				num_klik += 1

				if num_klik == 2:
					card_turned += 1	# player accumulates a turn
					num_klik = 0		# number of click resets

				if state == 0:	# no card revealed
					state = 1	# reveal the clicked card
					exposed_card[cnt][0] = True
				
				elif state == 1:	# 1 card revealed
					state = 2		# 2 cards revealed
					exposed_card[cnt][0] = True
					match_maker2()
				else:
					exposed_card[cnt][0] = True
					match_maker3(cnt)

		cnt += 1

	label.set_text("Turn = " + str(card_turned))


def draw(canvas):
	global card_deck, cardLoc
	global mouseklik_pos, exposed_card

	# draw cards
	cnt = 0			# index used in loop
	for lst in cardLoc:
		if not exposed_card[cnt][0]:	# card not exposed
			# cardPoints = [[lst[0], lst[1]], [lst[0]+CARD_WIDTH, lst[1]], [lst[0]+CARD_WIDTH, lst[1]+CARD_HEIGHT], [lst[0], lst[1]+CARD_HEIGHT]]
			# canvas.draw_polygon(cardPoints, 2, CARD_COLOUR, CARD_COLOUR)
			
			dest_centre = (lst[0] + CARD_WIDTH/2, lst[1] + CARD_HEIGHT/2)
			canvas.draw_image(card_back_image, CARD_CENTRE, CARD_SIZE, dest_centre, CARD_SIZE)
			
		else:		# card exposed
			temp_text = str(card_deck[cnt])
			canvas.draw_text(temp_text, [lst[0] + CARD_WIDTH/4, lst[1] + CARD_HEIGHT], NUM_SIZE, 'white')

		cnt += 1	# increment the index

		
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 1188, 100)
frame.add_button("Reset", new_game, 80)
label = frame.add_label("Turn = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

