"""
week 3 mini project
Implementation of classic arcade game pong
Author:  Song, Jiawen (Terry)
"""

import simpleguitk as simplegui
import random

# initialise global variables
# canvas information constants
WIDTH = 600
HEIGHT = 400

BALL_RADIUS = 20

# paddle information constants
PAD_WIDTH = 8
PAD_HEIGHT = 80

LEFT_HIT = False
RIGHT_HIT = False
MISS_BALL = False

ball_pos = [WIDTH / 2, HEIGHT / 2]	# ball position
ball_vel = [0, 0]		# ball velocity

# the paddles only have linear movements, so position and velocity are numbers
Lpaddle_pos = 100		# left paddle position
Lpaddle_vel = 0		# left paddle velocity

Rpaddle_pos = 100		# right paddle position
Rpaddle_vel = 0		# right paddle velocity

Lscore = 0		# left player score
Rscore = 0		# right player score

"""
initialise ball_pos and ball_vel for new ball in the centre of the table
if direction is RIGHT, the ball's velocity is upper right, else upper left
"""
def spawn_ball(direction):
	global ball_pos, ball_vel	# these are stored as lists

	ball_pos = [WIDTH / 2, HEIGHT / 2]	# centre of board

	ball_vel[0] = random.randrange(2, 6)
	ball_vel[1] = random.randrange(-3, 4)

	if direction == 'left':
		ball_vel[0] = -1*ball_vel[0]
# end of spawn_ball

# helper functions

def PaddlesStay():
# performs collision check between paddles and the board
	global Lpaddle_pos, Rpaddle_pos
	global Lpaddle_vel, Rpaddle_vel
	
	if Lpaddle_pos <= 0:		# left upper bound
		Lpaddle_pos = 1
		Lpaddle_vel = 0		# stop the movement
	
	elif Lpaddle_pos >= (HEIGHT - PAD_HEIGHT):	# left lower bound
		Lpaddle_pos = HEIGHT - PAD_HEIGHT
		Lpaddle_vel = 0		# stop the movement
	
	if Rpaddle_pos <= 0:		# right upper bound
		Rpaddle_pos = 1
		Rpaddle_vel = 0		# stop the movement
	
	elif Rpaddle_pos >= (HEIGHT - PAD_HEIGHT):	# right lower bound
		Rpaddle_pos = HEIGHT - PAD_HEIGHT
		Rpaddle_vel = 0		# stop the movement
	# end of if-elif
# end of PaddlesStay

def BallHit():
# determine whether collision between ball and paddle occur
	global Lpaddle_pos, Rpaddle_pos, ball_pos, ball_vel
	global LEFT_HIT, RIGHT_HIT, MISS_BALL

	if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS):	# left limit
		if (ball_pos[1] <= (Lpaddle_pos+PAD_HEIGHT)) and (ball_pos[1] >= Lpaddle_pos):
			ball_vel[0] = -1.1*ball_vel[0]
			LEFT_HIT = True
			MISS_BALL = False
		else:
			LEFT_HIT = False
			MISS_BALL = True
		# end of if-else
	
	elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):	# right limit
		if (ball_pos[1] <= (Rpaddle_pos+PAD_HEIGHT)) and (ball_pos[1] >= Rpaddle_pos):
			ball_vel[0] = -1.1*ball_vel[0]
			RIGHT_HIT = True
			MISS_BALL = False
		else:
			RIGHT_HIT = False
			MISS_BALL = True
		# end of if-else
# end of BallHit

# define event handlers

def new_game():			# restart handler
	global Lpaddle_pos, Lpaddle_vel, Rpaddle_pos, Rpaddle_vel
	global Lscore, Rscore
	global LEFT_HIT, RIGHT_HIT, MISS_BALL

	Lpaddle_pos = 100
	Rpaddle_pos = 100

	Lpaddle_vel = 0
	Rpaddle_vel = 0

	Lscore = 0
	Rscore = 0
	
	MISS_BALL = False
	LEFT_HIT = False
	RIGHT_HIT = False

	which_way = random.randrange(1, 3)
	
	if which_way == 1:
		spawn_ball('left')
	else:
		spawn_ball('right')
# end of new_game

def draw(canvas):		# draw handler
	global Lscore, Rscore, Lpaddle_pos, Rpaddle_pos, ball_pos, ball_vel
	global Lpaddle_vel, Rpaddle_vel
	global MISS_BALL, LEFT_HIT, RIGHT_HIT

	# draw mid line and gutter lines
	canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "white")
	canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "white")
	canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "white")

	# update ball
	ball_pos[0] += ball_vel[0]	# horizontal component
	ball_pos[1] += ball_vel[1]	# vertical component

	BallHit()			# determine ball paddle collision

	if MISS_BALL:
		if RIGHT_HIT:	# right player wins the point
			Rscore += 1
			spawn_ball('right')
			RIGHT_HIT = False
			LEFT_HIT = True

		elif LEFT_HIT:	# left player wins the point
			Lscore += 1
			spawn_ball('left')
			LEFT_HIT = False
			RIGHT_HIT = True
	
		# reset
		MISS_BALL = False
		# end if-elif

	if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):		# reflect the ball when it hits top or bottom
		ball_vel[1] = -1*ball_vel[1]

	# draw ball
	canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'white', 'white')

	# update paddles' veritcal position, keep paddles on the screen
	Lpaddle_pos += Lpaddle_vel
	Rpaddle_pos += Rpaddle_vel

	# paddle board collision checks
	PaddlesStay()

	# draw paddles
	Lpad_points = [(0, Lpaddle_pos), (PAD_WIDTH, Lpaddle_pos), (PAD_WIDTH, Lpaddle_pos + PAD_HEIGHT), (0, Lpaddle_pos + PAD_HEIGHT)]

	Rpad_points = [(WIDTH - PAD_WIDTH, Rpaddle_pos), (WIDTH, Rpaddle_pos), (WIDTH, Rpaddle_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, Rpaddle_pos + PAD_HEIGHT)]

	canvas.draw_polygon(Lpad_points, 1, 'Fuchsia', 'Fuchsia')
	canvas.draw_polygon(Rpad_points, 1, 'Aqua', 'Aqua')
	
	# draw scores
	canvas.draw_text(str(Lscore), (200, 50), 30, 'white')
	canvas.draw_text(str(Rscore), (400, 50), 30, 'white')

# end of draw

def keydown(key):
	step = 7
	global Lpaddle_vel, Rpaddle_vel

	if key == simplegui.KEY_MAP['W']:
		Lpaddle_vel = -1*step
	
	elif key == simplegui.KEY_MAP['S']:
		Lpaddle_vel = step

	elif key == simplegui.KEY_MAP['up']:
		Rpaddle_vel = -1*step

	elif key == simplegui.KEY_MAP['down']:
		Rpaddle_vel = step
	# end of if-elif-elif-elif
# end of keydown

def keyup(key):
	global Lpaddle_vel, Rpaddle_vel

	Lpaddle_vel = 0			# stop left paddle
	Rpaddle_vel = 0			# stop right paddle
# end of keyup

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESTART", new_game, 100)

# start frame
new_game()
frame.start()
