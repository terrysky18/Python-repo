"""
The explosion example in code skulptor
"""
import simpleguitk as simplegui

EXPLOSION_CENTRE = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]

explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# create timer that iterate current_sprite_centre through sprite
time = 0

# define draw handler
def draw(canvas):
	global time
	explosion_index = [time % EXPLOSION_DIM[0], (time // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
	canvas.draw_image(explosion_image,
			[EXPLOSION_CENTRE[0] + explosion_index[0] * EXPLOSION_SIZE[0],
			EXPLOSION_CENTRE[1] + explosion_index[1] * EXPLOSION_SIZE[1]],
			EXPLOSION_SIZE, EXPLOSION_CENTRE, EXPLOSION_SIZE)
	time += 1
# end of draw()

# create frame and size frame based on 100x100 pixel sprite
frame = simplegui.create_frame("Asteroid sprite", EXPLOSION_SIZE[0], EXPLOSION_SIZE[1])

# set draw handler and canvas background using custom HTML colour
frame.set_draw_handler(draw)
frame.set_canvas_background("blue")

# start animation
frame.start()

