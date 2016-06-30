##################################################
# Implementation of classic arcade game Pong
# By Chuck 10/13/2014
# No Unicorns or Rainbows included in this code, Just regular Pong
# ******  New and Improved Now with Auto Play!
###################################################
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
GUTTER = 10
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
# Paddle velocity when moving
PADDLE_SPEED = 10
# Speed up factor after each hit by a paddle
SPEED_UP = 1.2
# Auto Play
AUTO_PLAY = False

##########################################################
# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is right, else left
# The vertical Velocity is upwards
#########################################################
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [ -random.randrange(120, 240)/60.0 , -random.randrange(60, 180)/60.0]
    if direction:
        ball_vel[0] = -ball_vel[0]
        
 
#########################################################
# define event handlers
#########################################################

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global AUTO_PLAY # Reset out of Auto play
    score1 = 0
    score2 = 0
    paddle1_pos = [0, HEIGHT/2]
    paddle2_pos = [WIDTH, HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
    AUTO_PLAY = False
    spawn_ball(LEFT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
   
    # Update ball position
    ball_pos[0] = (ball_vel[0] + ball_pos[0])
    ball_pos[1] = (ball_vel[1] + ball_pos[1])
    if (ball_pos[0] <= BALL_RADIUS + GUTTER):
        #Possible scoring case check paddle position
        if abs(ball_pos[1] - paddle1_pos[1]) > HALF_PAD_HEIGHT:
            score2 += 1
            spawn_ball(RIGHT)
        else:
            ball_vel[0] = - ball_vel[0] * SPEED_UP
            ball_vel[1] = ball_vel[1] * SPEED_UP
        
    elif(ball_pos[0] >= (WIDTH - GUTTER - BALL_RADIUS)):
        # We have a possible scoring chance here check paddle position
        if abs(ball_pos[1] - paddle2_pos[1]) > HALF_PAD_HEIGHT:
            score1 += 1
            spawn_ball(LEFT)
        else:
            ball_vel[0] = - ball_vel[0] * SPEED_UP
            ball_vel[1] = ball_vel[1] * SPEED_UP

    # Check top or bottom contact 
    if ( ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - 1 - BALL_RADIUS)):
         ball_vel[1] = - ball_vel[1]
                                        

    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "Green")
   
    # update paddle's vertical position, keep paddle on the screen
    if not(AUTO_PLAY):
        paddle1_pos[1] += paddle1_vel
        paddle2_pos[1] += paddle2_vel
    else:
        paddle1_pos[1] = ball_pos[1]
        paddle2_pos[1] = ball_pos[1]
    # Check if paddle is pas the edge.  If so reset to at the edge
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    # draw paddles
    pad1_bot = [paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT]
    pad1_top = [paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT]
    pad2_bot = [paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT]
    pad2_top = [paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT]
    canvas.draw_line(pad1_bot, pad1_top, 2*PAD_WIDTH, 'White')
    canvas.draw_line(pad2_bot, pad2_top, 2*PAD_WIDTH, 'White')
    # draw scores
    canvas.draw_text(str(score1),(200,75),100,"Green")
    canvas.draw_text(str(score2),(350,75),100,"Green")
######################################################
# Key board handler
######################################################
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PADDLE_SPEED        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0      
##################################################
# Button Handler
##################################################
def auto_button():
    global AUTO_PLAY
    if AUTO_PLAY:
        AUTO_PLAY = False
        button2.set_text('Auto_Play')
    else:
       button2.set_text('Auto_Play Off')
       AUTO_PLAY = True


##################################################
# create frame
##################################################
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('New Game', new_game)
button2 = frame.add_button('Auto_Play', auto_button)
##################################################
# start frame
##################################################
new_game()
frame.start()
