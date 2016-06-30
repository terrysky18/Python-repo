# Mini-project 6 - Blackjack (simplistic)
# Author:  Song, Terry

import simpleguitk as simplegui
import random

# global constants
# load card sprite - 936x384, source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTRE = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTRE = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

CARD_GAP = 30
PLAYER_CARD_CENTRE = (85, 450)
DEALER_CARD_CENTRE = (85, 238)

# initialise some useful global variable
in_play = False			# a game is ongoing or not
question = ""			# question to the player
outcome = ""			# the outcome for the player
score = 0				# player score
forfeit = 0				# forfeit current game

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
# rank is the key to values dictionary
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define the card class
class Card:
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self.suit = suit
			self.rank = rank
		else:
			self.suit = None
			self.rank = None
			print "Invalid card: ", suit, rank
	
	def __str__(self):		# class output operator
		return self.suit + self.rank

	def get_suit(self):
		return self.suit

	def get_rank(self):
		return self.rank

	def draw(self, canvas, pos):
		card_loc = (CARD_CENTRE[0] + CARD_SIZE[0] * RANKS.index(self.rank),	# x component
				CARD_CENTRE[1] + CARD_SIZE[1] * SUITS.index(self.suit))		# y component
		
		canvas.draw_image(card_images, card_loc, CARD_SIZE,
				[pos[0] + CARD_CENTRE[0], pos[1] + CARD_CENTRE[1]], CARD_SIZE)
	
	def draw_card_back(self, canvas, pos):
		canvas.draw_image(card_back, CARD_BACK_CENTRE, CARD_SIZE,
				[pos[0] + CARD_BACK_CENTRE[0], pos[1] + CARD_BACK_CENTRE[1]], CARD_SIZE)

# define the hand class
class Hand:
# Hand class is a list of Card type
	def __init__(self):
		self.hand = []
		
	def __str__(self):
		card_hand = ''
		for single in self.hand:
			card_hand += str(single)
			card_hand += '\n'
		
		return card_hand
		
	def add_card(self, card):
		self.hand.append(card)
		
	def get_value(self):
	# check if there's an ace in the hand
	# if no, simply add the values of the cards
	# if yes,  determine if using Ace as 11 will bust
		hand_value = 0
		no_Ace = True
		
		for single in self.hand:
			hand_value += VALUES[single.get_rank()]
			if single.get_rank() == 'A':
				no_Ace = False		# there's an Ace in the hand
		
		if no_Ace:
			return hand_value
		else:
			if (hand_value + 10) <= 21:
				return hand_value + 10	# use Ace as 11
			else:
				return hand_value		# use Ace as 1
		
	def draw(self, canvas, pos):
		move = 0
		for single in self.hand:
			card_pos = [pos[0] + move * (CARD_GAP + CARD_SIZE[0]), pos[1]]
			single.draw(canvas, card_pos)
			move += 1
		
# define the pack class
class Pack:
	def __init__(self, suits, ranks):
		self.pack = []
		for i in suits:
			for j in ranks:
				single = Card(i, j)		# a single card in a pack
				self.pack.append(single)

	def shuffle(self):
		random.shuffle(self.pack)
		
	def deal_card(self):
		return self.pack.pop(0)			# remove and return the first in the pack
		
	def __str__(self):
		card_pack = ''
		for single in self.pack:
			card_pack += str(single)
			card_pack += '\n'
		
		return card_pack

# define event handlers for buttons
def deal():
# deal button shuffles the card pack and distributes cards to
# hands of player and dealer
	global outcome, in_play, question, forfeit, score
	global table_pack, player_hand, dealer_hand
	
	if (not in_play) and (forfeit == 0):
		# reinitialise pack of cards, needed to avoid exhausting a pack after multiple games
		table_pack = Pack(SUITS, RANKS)
		table_pack.shuffle()
		in_play = True
		question = "Hit or Stand"
		outcome = ""
		forfeit = 0
		
		# reinitialise hands, otherwise each game's hand accumulates
		player_hand = Hand()
		dealer_hand = Hand()
		
		card_dealt = table_pack.deal_card()		# first card
		player_hand.add_card(card_dealt)
		card_dealt = table_pack.deal_card()		# second card
		player_hand.add_card(card_dealt)
		
		card_dealt = table_pack.deal_card()		# first card
		dealer_hand.add_card(card_dealt)
		card_dealt = table_pack.deal_card()		# second card
		dealer_hand.add_card(card_dealt)
	else:
		if forfeit < 1:
			question = "Want to forfeit the game?\nclick once more to confirm"
			forfeit += 1
		else:
			score -= 1
			forfeit = 0			# reset forfeit
			in_play = False		# game forfeited
			deal()

def hit():
# if the hand is in play, hit the player
# if busted assign a message to outcome, update in_play and score
	global table_pack, player_hand
	global in_play, score, question, outcome, forfeit
	
	if forfeit > 0:
		forfeit = 0				# continue playing
		question = ""
	
	if in_play:
		card_dealt = table_pack.deal_card()
		player_hand.add_card(card_dealt)
	
		if player_hand.get_value() <= 21:
			# print "Your hand %d" % player_hand.get_value()
			pass
		else:
			in_play = False
			score -= 1
			outcome = "You have busted"
			question = "Deal again?"

def stand():
# if the hand is in play, repeatedly hit dealer until his hand value reaches 17 or more
# assign a message to outcome, update in_play and score
	global dealer_hand, table_pack, player_hand
	global outcome, in_play, score, question, forfeit
	
	if forfeit > 0:
		forfeit = 0				# continue playing
		question = ""
	# print "Your hand %d" % player_hand.get_value()
	
	if in_play:
		while dealer_hand.get_value() <= 17:
			card_dealt = table_pack.deal_card()
			dealer_hand.add_card(card_dealt)
	
		# print "Dealer's hand %d" % dealer_hand.get_value()
		if dealer_hand.get_value() <= 21:
			if dealer_hand.get_value() > player_hand.get_value():			
				outcome = "You lost"
				question = "Deal again?"
				score -= 1
			elif dealer_hand.get_value() == player_hand.get_value():
				outcome = "Tie, dealer wins"
				question = "One more?"
				score -= 1
			else:			
				outcome = "You win"
				question = "New deal?"
				score += 1
		else:
			outcome = "Dealer has busted"
			question = "New deal?"
			score += 1
		
		in_play = False			# player's hand is done

# draw handler
def draw(canvas):
	global outcome, question
	canvas.draw_text('Blackjack', (330, 110), 20, 'navy')
	canvas.draw_text('Score: ', (550, 80), 18, 'black', 'monospace')
	canvas.draw_text(str(score), (630, 80), 18, 'black', 'monospace')
	canvas.draw_text('Dealer', (80, 220), 20, 'black', 'sans-serif')
	canvas.draw_text('Player', (80, 428), 20, 'black', 'sans-serif')
	canvas.draw_text(outcome, (230, 220), 20, 'black', 'monospace')
	canvas.draw_text(question, (230, 428), 20, 'black', 'monospace')
	
	#draw pack of overlapping cards
	card_back = Card('D', 'A')
	pos = [50, 35]
	card_back.draw_card_back(canvas, pos)
	time = 0
	while time < 12:
		pos[0] += 8
		card_back.draw_card_back(canvas, pos)
		time += 1

	if not in_play:
		dealer_hand.draw(canvas, DEALER_CARD_CENTRE)
	else:
		dealer_hand.draw(canvas, DEALER_CARD_CENTRE)
		card_back.draw_card_back(canvas, DEALER_CARD_CENTRE)
	player_hand.draw(canvas, PLAYER_CARD_CENTRE)
	
# global game variables
table_pack = Pack(SUITS, RANKS)		# pack of card on table
player_hand = Hand()	# player's hand
dealer_hand = Hand()	# dealer's hand

# initialise frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
