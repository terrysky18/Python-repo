# A simple example showing the ball motion with implicit timer

import simpleguitk as simplegui

# initialise global variables
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH/2, HEIGHT/2]
vel = [0.3, -0.5]		# pixels per update (1/60 seconds)

# define event handlers
def draw(canvas):
	# update ball position
	ball_pos[0] += vel[0]
	ball_pos[1] += vel[1]

	# when the ball moves out of bound
	if (ball_pos[0] > WIDTH) or (ball_pos[0] < 0):
		ball_pos[0] = ball_pos[0] % WIDTH
	elif (ball_pos[1] > HEIGHT) or (ball_pos[1] < 1):
		ball_pos[1] = ball_pos[1] % HEIGHT
	
	# draw the ball
	canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'red', 'white')

# create frame
frame = simplegui.create_frame('Motion', WIDTH, HEIGHT)

# register event handler
frame.set_draw_handler(draw)

# start frame
frame.start()
