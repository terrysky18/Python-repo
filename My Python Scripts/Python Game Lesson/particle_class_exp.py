# Particle class example used to stimulate diffusion of molecules

import simpleguitk as simplegui
import random

# global constants
WIDTH = 600
HEIGHT = 400
PARTICLE_RADIUS = 5
COLOUR_LIST = ["red", "green", "blue", "white"]
DIRECTION_LIST = [[1, 0], [0, 1], [-1, 0], [0, -1]]

# particle class definition
class Particle:

	#initialiser for particles
	def __init__(self, position, colour):
		self.position = position
		self.colour = colour
	
	# updates position of a particle via vibration
	def move(self, vibration):
		self.position[0] += vibration[0]
		self.position[1] += vibration[1]
	
	# draw method for particles
	def draw(self, canvas):
		canvas.draw_circle(self.position, PARTICLE_RADIUS, 1,
				self.colour, self.colour)
	
	# string method for particle class
	def __str__(self):
		return "Particle with position = " + str(self.position) + " and colour = " + self.colour

# draw handler
def draw(canvas):
	for p in particle_list:		# particle_list is list of type Particle
		p.move(random.choice(DIRECTION_LIST))	# particle vibration
	
	for p in particle_list:
		p.draw(canvas)

# create frame and register draw handler
frame = simplegui.create_frame("Particle simulator", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# create a list of particles of the type Particle
particle_list = []
for i in range(50):
	p = Particle([WIDTH / 2, HEIGHT / 2], random.choice(COLOUR_LIST))
	particle_list.append(p)

# start frame
frame.start()

