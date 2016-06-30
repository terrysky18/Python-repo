# demo for drawing using tiled images

import simpleguitk as simplegui

# define globals for cards
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
SUITS = ('C', 'S', 'H', 'D')			# clubs, spades, hearts, diamonds

# card sprite - 950x392
CARD_CENTRE = (36.5, 49)	# centre of top left card, the 1st card
CARD_SIZE = (73, 98)		# size of all cards
# tiled image of all cards
card_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

# define card class
class Card:
	def __init__(self, suit, rank):
		self.rank = rank
		self.suit = suit

	def draw(self, canvas, loc):
		i = RANKS.index(self.rank)		# the indices are the multiples of
		j = SUITS.index(self.suit)		# 1st card centre coordinates
		card_pos = [CARD_CENTRE[0] + i * CARD_SIZE[0],
					CARD_CENTRE[1] + j * CARD_SIZE[1]]
		canvas.draw_image(card_image, card_pos, CARD_SIZE, loc, CARD_SIZE)

# define draw handler        
def draw(canvas):
	one_card.draw(canvas, (155, 90))

# define frame and register draw handler
frame = simplegui.create_frame("Card draw", 300, 200)
frame.set_draw_handler(draw)

# createa card
one_card = Card('H', 'K')

frame.start()
